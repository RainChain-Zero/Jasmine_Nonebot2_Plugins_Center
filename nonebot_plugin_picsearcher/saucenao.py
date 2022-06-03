from typing import List

from PicImageSearch import Network, SauceNAO
from PicImageSearch.model import SauceNAOResponse

from nonebot import get_driver, logger
from nonebot.adapters.mirai2 import MessageChain, Bot, MessageSegment
from .config import Config
from .utils import get_pic_b64, proxies, build_forward_message

global_config = get_driver().config
config = Config.parse_obj(global_config)

async def saucenao_search(bot: Bot, url: str) -> List:
    logger.info("sauceNAO引擎开始处理图片")
    async with Network(proxies=proxies) as client:
        saucenao = SauceNAO(client=client, api_key=config.saucenao_api_key)
        resp = await saucenao.search(url)

        rlimit = config.maxnum if len(
            resp.raw) >= config.maxnum else len(resp.raw)
        nodelist = [{
            "senderId": bot.self_id,
            "time": 0,
            "senderName": "茉莉",
            "messageChain": MessageChain([MessageSegment.plain("以下为SauceNAO的搜索结果")]),
            "messageId": None
        }]

        for i in range(0, rlimit):
            pic_b64 = await get_pic_b64(resp.raw[i].thumbnail)
            message_chain = MessageChain([MessageSegment.image(base64=pic_b64),
                                          MessageSegment.plain(
                f"\n相似度:{resp.raw[i].similarity}%"),
                MessageSegment.plain(
                f"\n标题：{resp.raw[i].title} | 作者：{resp.raw[i].author}\n地址：{resp.raw[i].url}")
            ])
            nodelist = await build_forward_message(bot, message_chain, nodelist)
        return nodelist
