from base64 import b64encode
import hashlib
import json
from typing import List
import aiofiles
import aiohttp
from nonebot import Bot, get_driver

from nonebot.adapters.mirai2 import MessageChain, MessageEvent, MessageSegment
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

proxies = "http://127.0.0.1:15732"


async def get_pic_b64(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxies) as resp:
            return b64encode(await resp.read()).decode("utf-8")


def build_forward_message(bot: Bot, msg_chain: MessageChain, nodelist: List) -> List:
    data = {
        "senderId": bot.self_id,
        "time": 0,
        "senderName": "茉莉",
        "messageChain": msg_chain,
        "messageId": None
    }
    nodelist.append(data)
    return nodelist


def forward_message_init(bot: Bot, engine: str) -> List:
    return [{
        "senderId": bot.self_id,
        "time": 0,
        "senderName": "茉莉",
        "messageChain": MessageChain([MessageSegment.plain(f"以下为{engine}的搜索结果")]),
        "messageId": None
    }]


async def download_pic(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            fileName = config.cache_path + "\\" + \
                hashlib.sha256(url.encode('utf-8')).hexdigest()+'.jpg'
            async with aiofiles.open(fileName, 'wb') as afp:
                await afp.write(await response.content.read())
                return fileName


def read_favor(qq: int) -> int:
    try:
        f = open(config.favor_path+str(qq)+config.favor_conf,
                 "r", encoding="utf-8")
    except:
        return 0
    json_str = f.read()
    f.close()
    j = json.loads(json_str)
    return j["好感度"] if j.__contains__("好感度") else 0
