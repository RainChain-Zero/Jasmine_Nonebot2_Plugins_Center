import json
from typing import List
import requests
import aiohttp
import asyncio
from PIL import Image, ImageFilter
import io
from nonebot import Bot, get_driver, logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from .config import Config

from ..utils.message import get_img

global_config = get_driver().config
config = Config.parse_obj(global_config)

# 判断数量是否超限


def judge_maxnum(num):
    if (num > config.maxnum):
        return False
    else:
        return True

# 判断群是否具有权限


def judge_group_permission(group: int) -> bool:
    try:
        f = open(config.group_permission_path, "r", encoding="utf-8")
    except:
        logger.error("nonebot_plugin_setu:找不到群权限配置文件")
        return False
    json_str = f.read()
    f.close()
    j = json.loads(json_str)
    for g in j["group_list"]:
        if (group == g):
            return True
    return False


async def call_setu_api(num: int, args: List = []):
    res = requests.get(
        f"https://api.lolicon.app/setu/v2?proxy=i.pixiv.cat", params={'num': num, 'tag': args, 'r18': 2}).json()
    if (res["error"] != ""):
        raise Exception('lolicon api调用失败')

    async def build_msg(title, pid, url, r18):
        pic_list = Message()
        pic_list.append(MessageSegment.text(
            f"pid：{pid} title：{title}\n"))
        pic_bytes = await get_img(url, global_config.proxy)
        # r18模糊处理
        pic_list.append(MessageSegment.image(
            pic_bytes if not r18 else blur_pic(pic_bytes)))
        return pic_list

    corutine_list = [build_msg(data['title'], data['pid'], data["urls"]["original"], data['r18'])
                     for data in res['data']]
    return await asyncio.gather(*corutine_list)


async def call_moe_api(num: int = 1, tags: List = [], session: aiohttp.ClientSession = None):
    async with session.get('http://localhost:45445/randomMoe',
                           params={'num': num, 'tags': tags}) as response:
        res = await response.json()
        if not res['succ']:
            raise Exception('茉莉后台api请求出错')
        return res['data']


async def get_pivix_pic(pid: int, r18: bool,  session: aiohttp.ClientSession) -> MessageSegment:
    headers = {'Referer': 'https://www.pixiv.net/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    logger.info(f'nonebot_plugin_setu:正在获取pid:{pid}的图片')
    async with session.get(f'https://www.pixiv.net/ajax/illust/{pid}/pages?lang=zh',
                           headers=headers, ssl=False,
                           proxy=global_config.proxy, cookies={'PHPSESSID': config.PHPSESSID}) as response:
        pic_url = await response.json()
        pic_url = pic_url['body'][0]['urls']['original']
        logger.info(f'nonebot_plugin_setu: 图片url:{pic_url}')
        async with session.get(pic_url, headers=headers, ssl=False, proxy=global_config.proxy) as response:
            pic_ori = await response.content.read()
            # r18模糊处理
            return f'pid:{pid}\n'+MessageSegment.image(pic_ori if not r18 else blur_pic(pic_ori))+'\n'


def blur_pic(pic_ori: bytes) -> bytes:
    img = Image.open(io.BytesIO(pic_ori))
    img = img.filter(ImageFilter.GaussianBlur(radius=50))
    out = io.BytesIO()
    img.save(out, format='png')
    return out.getvalue()
