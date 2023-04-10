import aiohttp
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, MessageEvent, GroupMessageEvent, Message
from nonebot.log import logger
from typing import List, Union


async def send_forward_msg(
    bot: Bot,
    event: MessageEvent,
    name: str,
    uin: str,
    msgs: List[Union[str, MessageSegment, Message]],
):
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    if isinstance(event, GroupMessageEvent):
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )


async def get_img(url: str, proxy: Union[str, None] = None, headers=None,ssl=True) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxy, headers=headers,ssl=ssl) as response:
            return await response.content.read()
