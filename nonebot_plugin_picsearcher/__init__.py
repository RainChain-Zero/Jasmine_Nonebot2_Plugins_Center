
import os
from nonebot import logger, on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.matcher import Matcher
from nonebot.matcher import Matcher
from nonebot.log import logger
from .utils import download_pic

from .functions import *

import nest_asyncio

from ..utils.data import read_favor
from ..utils.message import send_forward_msg
# 允许嵌套loop
nest_asyncio.apply()

engine_dic = {"saucenao": saucenao_search, "tracemoe": tracemoe_search,
              "ascii2d": ascii2d_search_main, "iqdb": iqdb_search, "google": google_search,
              "baidu": baidu_search, "ehentai": ehentai_search}

saucenao_command = on_command("saucenao搜图")
tracemoe_command = on_command("tracemoe搜图")
ascii2d_command = on_command("ascii2d搜图")
iqdb_command = on_command("iqdb搜图")
google_command = on_command("google搜图")
baidu_command = on_command("baidu搜图")
ehentai_command = on_command("ehentai搜图")
all_command = on_command("搜图")


@saucenao_command.handle()
@tracemoe_command.handle()
@ascii2d_command.handle()
@iqdb_command.handle()
@google_command.handle()
@baidu_command.handle()
@ehentai_command.handle()
@all_command.handle()
async def pic_search(bot: Bot, event: MessageEvent, matcher: Matcher):
    # 好感判断
    if read_favor(event.sender.user_id) < 2000:
        await matcher.finish("『×条件未满足』此功能要求好感度≥2000哦~")
    # 提取图片
    try:
        img_url = event.get_message()["image", 0].data["url"]
        logger.info(img_url)
    except:
        await matcher.finish(f"『×参数不足』当前消息中没有图片哦~")

    # 匹配搜索引擎
    message = event.get_plaintext()

    if event.get_plaintext().startswith("/搜图"):
        engine = "saucenao"
    else:
        engine = message[1:message.index("搜")].lower()
    await bot.send(event=event, message=f"『◎请稍后』茉莉正在处理图片...当前引擎{engine}")

    logger.info(f"搜图引擎：{engine}")
    if engine == "ascii2d":
        # 绕过QQ图片防盗链
        nodelist = await ascii2d_search_main(bot, f"https://images.weserv.nl/?url={img_url}")
    else:
        fileName = await download_pic(img_url)
        file = open(fileName, "rb")
        nodelist = await engine_dic[engine](bot, file)
        file.close()
        if os.path.exists(fileName):
            os.remove(fileName)
    await send_forward_msg(bot, event, '茉莉', bot.self_id, nodelist)
