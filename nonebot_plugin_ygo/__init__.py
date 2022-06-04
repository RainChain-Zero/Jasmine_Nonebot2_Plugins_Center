import aiohttp
import re
from nonebot import get_driver, logger, on_command

from .config import Config

from nonebot.adapters.mirai2 import MessageEvent, GroupMessage, FriendMessage, MessageSegment, Bot

global_config = get_driver().config
config = Config.parse_obj(global_config)

ygo_trigger = on_command("ygo", aliases={"YGO"})


@ygo_trigger.handle()
async def ygo(bot: Bot, event: MessageEvent):
    card_name = event.get_plaintext()[4:].strip()
    logger.info(card_name)
    # 获取图片url列表
    img_url = await ygo_search(card_name)
    # 结果为空
    if len(img_url) == 0:
        await ygo_trigger.finish("『×查询失败』茉莉未找到相关信息呢...")
    elif len(img_url) == 1:
        await ygo_trigger.finish(MessageSegment.image(url=img_url[0]))
    # 构造转发消息结点列表
    node_list = await build_forward_message(bot, img_url)
    if isinstance(event, GroupMessage):
        await bot.send_group_message(target=event.sender.group.id, message_chain=[{"type": "Forward", "nodeList": node_list}])
    elif isinstance(event, FriendMessage):
        await bot.send_friend_message(target=event.sender.id, message_chain=[{"type": "Forward", "nodeList": node_list}])


async def ygo_search(card_name: str):
    url = f"https://ygocdb.com/?search={card_name}"
    async with aiohttp.ClientSession() as session:
        res = await session.get(url=url)
        html_bytes = await res.content.read()
        html = html_bytes.decode()
        img_url = re.compile(r'<img data-original="(.*)!half"').findall(html)
    return img_url[:config.max_num]


async def build_forward_message(bot: Bot, img_url: list):
    node_list = []
    for img in img_url:
        data = {
            "senderId": bot.self_id,
            "time": 0,
            "senderName": "茉莉",
            "messageChain": [MessageSegment.image(url=img)],
            "messageId": None
        }
        node_list.append(data)
    return node_list
