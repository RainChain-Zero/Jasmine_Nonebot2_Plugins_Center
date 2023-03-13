from base64 import b64encode
import hashlib
import json
from typing import List
import aiofiles
import aiohttp
from nonebot import Bot, get_driver

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

proxies = global_config.proxy


async def download_pic(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            fileName = config.cache_path + "\\" + \
                hashlib.sha256(url.encode('utf-8')).hexdigest()+'.jpg'
            async with aiofiles.open(fileName, 'wb') as afp:
                await afp.write(await response.content.read())
                return fileName
