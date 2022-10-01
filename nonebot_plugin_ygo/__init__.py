import aiohttp
import re
from nonebot import get_driver, logger, on_command

from .config import Config

from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, PrivateMessageEvent, MessageSegment, Bot
from ..utils.message import *
global_config = get_driver().config
config = Config.parse_obj(global_config)

ygo_trigger = on_command("ygo", aliases={"YGO"})


@ygo_trigger.handle()
async def ygo(bot: Bot, event: MessageEvent):
    card_name = event.get_plaintext()[4:].strip()
    # 获取图片url列表
    img_url = await ygo_search(card_name)
    # 结果为空
    if len(img_url) == 0:
        await ygo_trigger.finish("『×查询失败』茉莉未找到相关信息呢...")
    elif len(img_url) == 1:
        await ygo_trigger.finish(MessageSegment.image(await get_img(img_url[0])))
    # 构造转发消息结点列表
    node_list = [MessageSegment.image(await get_img(url)) for url in img_url]
    await send_forward_msg(bot, event, '茉莉', bot.self_id, node_list)


async def ygo_search(card_name: str):
    url = f"https://ygocdb.com/?search={card_name}"
    async with aiohttp.ClientSession() as session:
        res = await session.get(url=url)
        html_bytes = await res.content.read()
        html = html_bytes.decode()
        img_url = re.compile(r'<img data-original="(.*)!half"').findall(html)
    return img_url[:config.max_num]
