from base64 import b64encode
from typing import List
import aiohttp

from nonebot.adapters.mirai2 import Bot,MessageChain

proxies = "http://127.0.0.1:15732"

async def get_pic_b64(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxies) as resp:
            return b64encode(await resp.read()).decode("utf-8")

async def build_forward_message(bot: Bot, msg_chain: MessageChain, nodelist: List) -> List:
    data = {
        "senderId": bot.self_id,
        "time": 0,
        "senderName": "茉莉",
        "messageChain": msg_chain,
        "messageId": None
    }
    nodelist.append(data)
    return nodelist