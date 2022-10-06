import re
from asyncio import TimeoutError
from urllib import parse

from aiohttp import ContentTypeError
from nonebot import on_regex, on_command, logger
from nonebot.adapters.onebot.v11 import Bot, utils, GroupMessageEvent, GROUP
from nonebot.internal.matcher import Matcher
from nonebot.typing import T_State

from .config import Config
from .constants import ARTICLE_RAW, ARTICLE, RAW, TEMPLATE
from .exception import NoDefaultPrefixException, NoSuchPrefixException

__all__ = ['wiki_preprocess', 'wiki_parse']

from .fakemwapi import DummyMediaWiki, DummyPage

from .mediawiki import MediaWiki, HTTPTimeoutError, MediaWikiException, MediaWikiGeoCoordError, PageError, \
    DisambiguationError
from .mediawiki.exceptions import InterWikiError, MediaWikiAPIURLError, MediaWikiBaseException

# 已有的MediaWiki实例
wiki_instances = {}


# 响应器
wiki_article = on_regex(ARTICLE_RAW, permission=GROUP, state={"mode": "article"})
wiki_template = on_regex(TEMPLATE, permission=GROUP, state={"mode": "template"})
wiki_raw = on_regex(RAW, permission=GROUP, state={"mode": "raw"})
wiki_quick = on_command("wiki ", permission=GROUP, state={"mode": "quick"})


@wiki_article.handle()
@wiki_template.handle()
@wiki_raw.handle()
@wiki_quick.handle()
async def wiki_preprocess(bot: Bot, event: GroupMessageEvent, state: T_State, matcher: Matcher):
    message = utils.unescape(str(event.message).strip())
    mode = state["mode"]
    if mode == "article":
        title = re.findall(ARTICLE, message)
    elif mode == "template":
        title = re.findall(TEMPLATE, message)
        state["is_template"] = True
    elif mode == "raw":
        title = re.findall(RAW, message)
        state["is_raw"] = True
    else:
        title = message[4:].lstrip()
        if not title:
            await matcher.finish()
        title = [title]

    if not title:
        await matcher.finish()
    state["title"] = title[0]
    state["is_user_choice"] = False


@wiki_article.got("title", "请从上面选择一项，或回复0来根据原标题直接生成链接，回复”取消“退出")
@wiki_template.got("title", "请从上面选择一项，或回复0来根据原标题直接生成链接，回复”取消“退出")
@wiki_raw.got("title", "请从上面选择一项，或回复0来根据原标题直接生成链接，回复”取消“退出")
@wiki_quick.got("title", "请从上面选择一项，或回复0来根据原标题直接生成链接，回复”取消“退出")
async def wiki_parse(bot: Bot, event: GroupMessageEvent, state: T_State, matcher: Matcher):
    # 标记
    page = None
    exception = None

    if state.get("is_user_choice"):  # 选择模式，获取先前存储的数据
        msg = str(state["title"]).strip()
        if (not msg.isdigit()) or int(msg) not in range(len(state["options"]) + 1):  # 非选择项或超范围
            await matcher.finish()

        choice = int(msg)
        if not choice:  # 选0，直接生成链接
            if state.get("disambiguation"):
                page = DummyPage(state['disambiguation'].url, state['raw_title'])
            else:
                instance = state["dummy_instance"]
                page = await instance.page(state["raw_title"])
        else:
            title = state["options"][choice - 1]
            wiki_instance = state["instance"]
            dummy_instance = state["dummy_instance"]
            api = state["api"]
    else:
        config = Config(event.group_id)
        title = state["title"]
        prefix = re.match(r'\w+:|\w+：', title)
        if not prefix:
            prefix = ''
        else:
            prefix = prefix.group(0).lower().rstrip(":：")
            if prefix in config.prefixes:
                title = re.sub(f"{prefix}:|{prefix}：", '', title, count=1, flags=re.I)
            else:
                prefix = ''

        if title is None or title.strip() == "":
            await matcher.finish()

    # 检查锚点
    anchor_list = re.split('#', title, maxsplit=1)
    title = anchor_list[0]
    state["anchor"] = anchor_list[1] if len(anchor_list) > 1 else state.get("anchor")

    if not state.get("is_user_choice"):
        if state.get("is_template"):
            title = "Template:" + title
        try:
            api, url = config.get_from_prefix(prefix)[:2]
        except NoDefaultPrefixException:
            await matcher.finish("没有找到默认前缀，请群管或bot管理员先设置默认前缀")
            return
        except NoSuchPrefixException:
            await matcher.finish("指定的默认前缀对应的wiki不存在，请管理员检查设置")
            return

        state["api"] = api  # 选择模式下，不会主动读取配置，因此需要提供api地址供生成链接

        dummy_instance = DummyMediaWiki(url)  # 用于生成直链的MediaWiki实例
        if state.get("is_raw"):
            wiki_instance = dummy_instance
        else:
            # 获取已有的MediaWiki实例，以api链接作为key
            global wiki_instances
            if api in wiki_instances.keys():
                wiki_instance = wiki_instances[api]
            else:
                if api:
                    try:
                        wiki_instance = await MediaWiki.create(url=api)
                        wiki_instances[api] = wiki_instance
                    except (MediaWikiBaseException, TimeoutError) as e:
                        logger.info(f"连接到MediaWiki API 时发生了错误：{e}")
                        exception = "连接超时"
                        wiki_instance = dummy_instance
                else:  # 没api地址就算了
                    wiki_instance = dummy_instance

    if not page:
        try:
            page = await wiki_instance.page(title=title, auto_suggest=False, convert_titles=True, iwurl=True)
            exception = exception or None
        except (HTTPTimeoutError, TimeoutError):
            exception = "连接超时"
            page = await dummy_instance.page(title=title)
        except (MediaWikiException, MediaWikiGeoCoordError, ContentTypeError) as e:  # ContentTypeError：非json内容
            exception = "Api调用出错"
            logger.info(f"MediaWiki API 返回了错误信息：{e}")
            page = await dummy_instance.page(title=title)
        except PageError:
            try:
                search = await wiki_instance.search(title)
                if search:
                    result = f"页面 {title} 不存在；你是不是想找："
                    for k, v in enumerate(search):
                        result += f"\n{k + 1}. {v}"
                    state["is_user_choice"] = True
                    state["options"] = search
                    state["raw_title"] = title
                    state["instance"] = wiki_instance
                    state["dummy_instance"] = dummy_instance
                    state.pop("title")
                    await matcher.reject(result)
                    return  # 同理，糊弄下IDE
                else:
                    page = await dummy_instance.page(title=title)
            except (MediaWikiBaseException, TimeoutError):
                page = await dummy_instance.page(title=title)
            exception = "未找到页面"
        except DisambiguationError as e:
            result = f"条目 {e.title} 是一个消歧义页面，有以下含义："
            for k, v in enumerate(e.options):
                result += f"\n{k + 1}. {v}"
            state["is_user_choice"] = True
            state["disambiguation"] = e
            state["options"] = e.options
            state["raw_title"] = title
            state["instance"] = wiki_instance
            state["dummy_instance"] = dummy_instance
            state.pop("title")
            await matcher.reject(result)
            return
        except InterWikiError as e:
            result = f"跨维基链接：{e.title}\n" \
                     f"链接：{e.url}"
            await matcher.finish(result)
            return
        except Exception as e:
            exception = "未知错误"
            logger.warning(f"MediaWiki API 发生了未知异常：{e}")
            page = dummy_instance.page(title=title)

    result = f"错误：{exception}\n" if exception else ""
    if page.title != title:
        result += f"重定向 {title} → {page.title}\n"
    else:
        result += f"标题：{page.title}\n"
    if hasattr(page, "pageid"):
        result += f"链接：{api[:-7]}index.php?curid={page.pageid}"  # 使用页面id来缩短链接
    else:
        result += f"链接：{page.url}"
    if state.get("anchor"):
        result += parse.quote("#" + state["anchor"])

    await matcher.finish(result)
