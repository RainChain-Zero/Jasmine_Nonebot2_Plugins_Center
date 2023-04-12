
from io import BytesIO
from typing import List
from xmlrpc.client import Boolean

from PicImageSearch import Network, SauceNAO, SauceNAO, TraceMoe, Ascii2D, Iqdb, Google, BaiDu, EHentai
from nonebot import Bot, get_driver, logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from .config import Config
from .utils import proxies

from ..utils.message import get_img

global_config = get_driver().config
config = Config.parse_obj(global_config)


async def saucenao_search(bot: Bot, file: BytesIO):
    logger.info(f"sauceNAO引擎开始处理图片")
    nodelist = [MessageSegment.text("以下为sauceNAO的搜索结果")]
    try:
        async with Network(proxies=proxies) as client:
            saucenao = SauceNAO(
                client=client, api_key=config.saucenao_api_key)
            resp = await saucenao.search(file=file.read())
            rlimit = config.maxnum if len(
                resp.raw) >= config.maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if resp.raw[i].thumbnail != "":
                    pic_bytes = await get_img(resp.raw[i].thumbnail)
                    message_chain = Message([MessageSegment.image(pic_bytes),
                                             MessageSegment.text(
                        f"\n相似度:{resp.raw[i].similarity}%"),
                        MessageSegment.text(
                        f"\n标题：{resp.raw[i].title} | 作者：{resp.raw[i].author}\n地址：{resp.raw[i].url}")
                    ])
                else:
                    rlimit = rlimit + 1
                    continue
                nodelist.append(message_chain)
    except Exception as e:
        logger.error(f"saucenao搜图失败！{e}")
        nodelist = Message([MessageSegment.text("『×Error』saucenao搜图失败，请稍后再试")])
    return nodelist


async def tracemoe_search(bot: Bot, file: BytesIO):
    logger.info(f"tracemoe引擎开始处理图片")
    nodelist = [MessageSegment.text("以下为tracemoe的搜索结果")]
    try:
        async with Network(proxies=proxies) as client:
            tracemoe = TraceMoe(client=client, mute=False,
                                size=None)
            resp = await tracemoe.search(file=file.read())
            rlimit = config.maxnum if len(
                resp.raw) >= config.maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if resp.raw[i].image != "":
                    pic_bytes = await get_img(resp.raw[i].image)
                    starts = int(resp.raw[i].From)
                    startm = int(starts/60)
                    starth = int(starts/3600)
                    starts = starts % 60
                    ends = int(resp.raw[i].To)
                    endm = int(ends/60)
                    endh = int(ends/3600)
                    ends = ends % 60
                    message_chain = Message([MessageSegment.text(
                        f"番名：{resp.raw[i].title_chinese} 第{resp.raw[i].episode}集\n出现在：{starth}:{startm}:{starts}~{endh}:{endm}:{ends}\n相似度：{resp.raw[i].similarity}%\n"),
                        MessageSegment.image(pic_bytes)])
                else:
                    rlimit = rlimit + 1
                    continue
                nodelist.append(message_chain)
    except Exception as e:
        logger.error(f"tracemoe搜图失败！{e}")
        nodelist = Message([MessageSegment.text("『×Error』tracemoe搜图失败，请稍后再试")])
    return nodelist


async def ascii2d_search(bot: Bot, url: str, bovm: Boolean):
    name = "特征" if bovm else "色彩"
    logger.info(f"ascii2{name}检索引擎开始处理图片")
    nodelist = [MessageSegment.text(f"以下为ascii2{name}的搜索结果")]
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
                pic_bytes = await get_img(resp.raw[i].thumbnail)
                message_chain = Message([MessageSegment.text(
                    f"标题：{resp.raw[i].title} 作者：{resp.raw[1].author}\nurl：{resp.raw[i].url}\n"),
                    MessageSegment.image(pic_bytes)])
                nodelist.append(message_chain)
    except Exception as e:
        logger.error(f"ascii2d{name}引擎搜图失败！{e}")
        nodelist = Message([MessageSegment.text(
            f"『×Error』ascii2d{name}搜图失败，请稍后再试")])
    return nodelist


async def ascii2d_search_main(bot: Bot, url: str):
    try:
        color = await ascii2d_search(bot, url, False)
        character = await ascii2d_search(bot, url, True)
        nodelist = color + character
    except:
        logger.error("ascii2d所有搜索引擎搜图失败！")
    return nodelist


async def iqdb_search(bot: Bot, file: BytesIO):
    logger.info("iqdb引擎开始处理图片")
    nodelist = [MessageSegment.text(f"以下为Iqdb的搜索结果")]
    try:
        async with Network(proxies=proxies) as client:
            iqdb = Iqdb(client=client)
            resp = await iqdb.search(file=file.read())

            rlimit = config.maxnum if len(
                resp.raw) >= config.maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if resp.raw[i].thumbnail != "":
                    pic_bytes = await get_img(resp.raw[i].thumbnail)
                    message_chain = Message([MessageSegment.text(
                        f"来源平台：{resp.raw[i].source}\nurl：{resp.raw[0].url}\n相似度：{resp.raw[i].similarity}\n"), MessageSegment.image(pic_bytes)])
                else:
                    rlimit = rlimit + 1
                    continue
                nodelist.append(message_chain)
    except Exception as e:
        logger.error(f"iqdb引擎搜图失败！{e}")
        nodelist = Message([MessageSegment.text("『×Error』iqdb搜图失败，请稍后再试")])
    return nodelist


async def google_search(bot: Bot, file: BytesIO):
    logger.info("Google引擎开始处理图片")
    nodelist = [MessageSegment.text(f"以下为Google的搜索结果")]
    try:
        async with Network(proxies=proxies) as client:
            google = Google(client=client)
            resp = await google.search(file=file.read())
            rlimit = config.google_baidu_maxnum if len(
                resp.raw) - 2 >= config.google_baidu_maxnum else len(resp.raw) - 2
            for i in range(2, 2 + rlimit):
                if resp.raw[i].thumbnail != "":
                    pic_bytes = await get_img(resp.raw[i].thumbnail)
                    message_chain = Message([MessageSegment.text(
                        f"标题：{resp.raw[i].title}\nurl：{resp.raw[i].url}\n"), MessageSegment.image(pic_bytes)])
                    nodelist.append(message_chain)
                else:
                    message_chain = Message([MessageSegment.text(
                        f"标题：{resp.raw[i].title}\nurl：{resp.raw[i].url}\n")])
                    nodelist.append(message_chain)
    except Exception as e:
        logger.error(f"Google引擎搜图失败！{e}")
        nodelist = Message([MessageSegment.text("『×Error』Google搜图失败，请稍后再试")])
    return nodelist


async def baidu_search(bot: Bot, file: BytesIO):
    logger.info("百度引擎开始处理图片")
    nodelist = [MessageSegment.text(f"以下为百度的搜索结果")]
    try:
        async with Network() as client:
            baidu = BaiDu(client=client)
            resp = await baidu.search(file=file.read())
            if resp.same == None:
                return Message([MessageSegment.text("百度识图未找到类似图片哦~")])
            rlimit = config.google_baidu_maxnum if len(
                resp.raw) >= config.google_baidu_maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if resp.raw[i].image_src != "":
                    pic_bytes = await get_img(resp.raw[i].image_src)
                    message_chain = Message([MessageSegment.text(
                        f"标题：{resp.raw[i].title}\nurl：{resp.raw[i].url}\n"), MessageSegment.image(pic_bytes)])
                else:
                    rlimit = rlimit + 1
                    continue
                nodelist.append(message_chain)
    except Exception as e:
        logger.error(f"百度引擎搜图失败！{e}")
        nodelist = Message([MessageSegment.text("『×Error』百度搜图失败，请稍后再试")])
    return nodelist


async def ehentai_search(bot: Bot, file: BytesIO) -> List:
    logger.info("E-Hentai引擎开始处理图片")
    nodelist = [MessageSegment.text(f"以下为E-Hentai的搜索结果")]
    try:
        async with Network(proxies=proxies, cookies=config.ehentai_cookies) as client:
            ehentai = EHentai(client=client)
            resp = await ehentai.search(file=file.read(), ex=False)
            rlimit = config.maxnum if len(
                resp.raw) >= config.maxnum else len(resp.raw)
            for i in range(0, rlimit):
                if resp.raw[i].thumbnail != "":
                    pic_bytes = await get_img(resp.raw[i].thumbnail)
                    message_chain = Message([MessageSegment.text(
                        f"标题：{resp.raw[i].title}\nurl：{resp.raw[i].url}\n分类：{resp.raw[i].type}\n"), MessageSegment.image(pic_bytes)])
                else:
                    rlimit = rlimit + 1
                    continue
                nodelist.append(message_chain)
    except Exception as e:
        logger.error("E-Hentai引擎搜图失败！{e}")
        nodelist = Message([MessageSegment.text("『×Error』ehentai搜图失败，请稍后再试")])
    return nodelist
