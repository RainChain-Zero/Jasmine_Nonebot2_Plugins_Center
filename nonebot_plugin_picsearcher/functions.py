
from asyncio import get_event_loop
import asyncio
from io import BytesIO
from typing import List
from xmlrpc.client import Boolean

from PicImageSearch import Network, SauceNAO, SauceNAO, TraceMoe, Ascii2D, Iqdb, Google, BaiDu, EHentai
from nonebot import Bot, get_driver, logger
from nonebot.adapters.mirai2 import MessageChain, MessageSegment
from .config import Config
from .utils import forward_message_init, get_pic_b64, proxies, build_forward_message

global_config = get_driver().config
config = Config.parse_obj(global_config)


async def saucenao_search(bot: Bot, file: BytesIO) -> List:
    logger.info(f"sauceNAO引擎开始处理图片")
    nodelist = forward_message_init(bot, "saucenao")
    try:
        async with Network(proxies=proxies) as client:
            saucenao = SauceNAO(
                client=client, api_key=config.saucenao_api_key)
            resp = await saucenao.search(file=file)
            rlimit = config.maxnum if len(
                resp.raw) >= config.maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if resp.raw[i].thumbnail != "":
                    pic_b64 = await get_pic_b64(resp.raw[i].thumbnail)
                    message_chain = MessageChain([MessageSegment.image(base64=pic_b64),
                                                  MessageSegment.plain(
                        f"\n相似度:{resp.raw[i].similarity}%"),
                        MessageSegment.plain(
                        f"\n标题：{resp.raw[i].title} | 作者：{resp.raw[i].author}\n地址：{resp.raw[i].url}")
                    ])
                else:
                    rlimit = rlimit + 1
                    continue
                nodelist = build_forward_message(bot, message_chain, nodelist)
    except:
        logger.error("saucenao搜图失败！")
        nodelist = build_forward_message(
            bot, MessageChain([MessageSegment.plain("『×Error』saucenao搜图失败，请稍后再试")]), nodelist)
    return nodelist


async def tracemoe_search(bot: Bot, file: BytesIO) -> List:
    logger.info(f"tracemoe引擎开始处理图片")
    nodelist = forward_message_init(bot, "tracemoe")
    try:
        async with Network(proxies=proxies) as client:
            tracemoe = TraceMoe(client=client, mute=False,
                                size=None)
            resp = await tracemoe.search(file=file)
            rlimit = config.maxnum if len(
                resp.raw) >= config.maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if resp.raw[i].image != "":
                    pic_b64 = await get_pic_b64(resp.raw[i].image)
                    starts = int(resp.raw[i].From)
                    startm = int(starts/60)
                    starth = int(starts/3600)
                    starts = starts % 60
                    ends = int(resp.raw[i].To)
                    endm = int(ends/60)
                    endh = int(ends/3600)
                    ends = ends % 60
                    message_chain = MessageChain([MessageSegment.plain(
                        f"番名：{resp.raw[i].title_chinese} 第{resp.raw[i].episode}集\n出现在：{starth}:{startm}:{starts}~{endh}:{endm}:{ends}\n相似度：{resp.raw[i].similarity}%\n"),
                        MessageSegment.image(base64=pic_b64)])
                else:
                    rlimit = rlimit + 1
                    continue
                nodelist = build_forward_message(bot, message_chain, nodelist)
    except:
        logger.error("tracemoe搜图失败！")
        nodelist = build_forward_message(
            bot, MessageChain([MessageSegment.plain("『×Error』tracemoe搜图失败，请稍后再试")]), nodelist)
    return nodelist


async def ascii2d_search(bot: Bot, url: str, bovm: Boolean) -> List:
    name = "特征" if bovm else "色彩"
    logger.info(f"ascii2{name}检索引擎开始处理图片")
    nodelist = forward_message_init(bot, f"Ascii2d{name}检索")
    try:
        async with Network(proxies=proxies) as client:
            ascii2d = Ascii2D(client=client, bovw=bovm)
            resp = await ascii2d.search(url)
            rlimit = config.maxnum if len(
                resp.raw) >= config.maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if i == 0 and resp.raw[0].url == "":
                    rlimit = rlimit + 1
                    continue
                pic_b64 = await get_pic_b64(resp.raw[i].thumbnail)
                message_chain = MessageChain([MessageSegment.plain(
                    f"标题：{resp.raw[i].title} 作者：{resp.raw[1].author}\nurl：{resp.raw[i].url}\n"),
                    MessageSegment.image(base64=pic_b64)])
                nodelist = build_forward_message(bot, message_chain, nodelist)
    except:
        logger.error(f"ascii2d{name}引擎搜图失败！")
        nodelist = build_forward_message(
            bot, MessageChain([MessageSegment.plain("f『×Error』ascii2d{name}搜图失败，请稍后再试")]), nodelist)
    return nodelist


async def ascii2d_search_main(bot: Bot, url: str) -> List:
    try:
        loop = asyncio.get_event_loop()
        color = asyncio.ensure_future(ascii2d_search(bot, url, False))
        character = asyncio.ensure_future(ascii2d_search(bot, url, True))
        # 并发执行色彩和特征检索
        loop.run_until_complete(asyncio.gather(color, character))
        nodelist = forward_message_init(bot, "ascii2d")
        color_forward = [{"type": "Forward", "nodeList": color.result()}]
        character_forward = [
            {"type": "Forward", "nodeList": character.result()}]
        nodelist = build_forward_message(bot, color_forward, nodelist)
        nodelist = build_forward_message(bot, character_forward, nodelist)
    except:
        logger.error("ascii2d所有搜索引擎搜图失败！")
    return nodelist


async def iqdb_search(bot: Bot, file: BytesIO) -> List:
    logger.info("iqdb引擎开始处理图片")
    nodelist = forward_message_init(bot, "Iqdb检索")
    try:
        async with Network(proxies=proxies) as client:
            iqdb = Iqdb(client=client)
            resp = await iqdb.search(file=file)

            rlimit = config.maxnum if len(
                resp.raw) >= config.maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if resp.raw[i].thumbnail != "":
                    pic_b64 = await get_pic_b64(resp.raw[i].thumbnail)
                    message_chain = MessageChain([MessageSegment.plain(
                        f"来源平台：{resp.raw[i].source}\nurl：{resp.raw[0].url}\n相似度：{resp.raw[i].similarity}\n"), MessageSegment.image(base64=pic_b64)])
                else:
                    rlimit = rlimit + 1
                    continue
                nodelist = build_forward_message(bot, message_chain, nodelist)
    except:
        logger.error("iqdb引擎搜图失败！")
        nodelist = build_forward_message(
            bot, MessageChain([MessageSegment.plain("『×Error』iqdb搜图失败，请稍后再试")]), nodelist)
    return nodelist


async def google_search(bot: Bot, file: BytesIO) -> List:
    logger.info("Google引擎开始处理图片")
    nodelist = forward_message_init(bot, "google")
    try:
        async with Network(proxies=proxies) as client:
            google = Google(client=client)
            resp = await google.search(file=file)
            rlimit = config.google_baidu_maxnum if len(
                resp.raw) - 2 >= config.google_baidu_maxnum else len(resp.raw) - 2
            for i in range(2, 2 + rlimit):
                if resp.raw[i].thumbnail != "":
                    pic_b64 = await get_pic_b64(resp.raw[i].thumbnail)
                    message_chain = MessageChain([MessageSegment.plain(
                        f"标题：{resp.raw[i].title}\nurl：{resp.raw[i].url}\n"), MessageSegment.image(base64=pic_b64)])
                    nodelist = build_forward_message(
                        bot, message_chain, nodelist)
                else:
                    message_chain = MessageChain([MessageSegment.plain(
                        f"标题：{resp.raw[i].title}\nurl：{resp.raw[i].url}\n")])
                    nodelist = build_forward_message(
                        bot, message_chain, nodelist)
    except:
        logger.error("Google引擎搜图失败！")
        nodelist = build_forward_message(
            bot, MessageChain([MessageSegment.plain("『×Error』Google搜图失败，请稍后再试")]), nodelist)
    return nodelist


async def baidu_search(bot: Bot, file: BytesIO) -> List:
    logger.info("百度引擎开始处理图片")
    nodelist = forward_message_init(bot, "baidu")
    try:
        async with Network(proxies=proxies) as client:
            baidu = BaiDu(client=client)
            resp = await baidu.search(file=file)
            if resp.same == None:
                return build_forward_message(bot, MessageChain([MessageSegment.plain("百度识图未找到类似图片哦~")]), nodelist)
            rlimit = config.google_baidu_maxnum if len(
                resp.raw) >= config.google_baidu_maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if resp.raw[i].image_src != "":
                    pic_b64 = await get_pic_b64(resp.raw[i].image_src)
                    message_chain = MessageChain([MessageSegment.plain(
                        f"标题：{resp.raw[i].title}\nurl：{resp.raw[i].url}\n"), MessageSegment.image(base64=pic_b64)])
                else:
                    rlimit = rlimit + 1
                    continue
                nodelist = build_forward_message(bot, message_chain, nodelist)
    except:
        logger.error("百度引擎搜图失败！")
        nodelist = build_forward_message(bot, MessageChain(
            [MessageSegment.plain("『×Error』百度搜图失败，请稍后再试")]))
    return nodelist


async def ehentai_search(bot: Bot, file: BytesIO) -> List:
    logger.info("E-Hentai引擎开始处理图片")
    nodelist = forward_message_init(bot, "ehentai")
    try:
        async with Network(proxies=proxies, cookies=config.ehentai_cookies) as client:
            ehentai = EHentai(client=client)
            resp = await ehentai.search(file=file, ex=False)
            rlimit = config.maxnum if len(
                resp.raw) >= config.maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if resp.raw[i].thumbnail != "":
                    pic_b64 = await get_pic_b64(resp.raw[i].thumbnail)
                    message_chain = MessageChain([MessageSegment.plain(
                        f"标题：{resp.raw[i].title}\nurl：{resp.raw[i].url}\n分类：{resp.raw[i].type}\n"), MessageSegment.image(base64=pic_b64)])
                else:
                    rlimit = rlimit + 1
                    continue
                nodelist = build_forward_message(bot, message_chain, nodelist)
    except:
        logger.error("E-Hentai引擎搜图失败！")
        nodelist = build_forward_message(bot, MessageChain(
            [MessageSegment.plain("『×Error』ehentai搜图失败，请稍后再试")]), nodelist)
    return nodelist