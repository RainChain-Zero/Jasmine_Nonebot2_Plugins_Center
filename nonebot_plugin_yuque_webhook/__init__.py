import json
from nonebot import get_driver, get_bot, logger
import nonebot
from .config import Config
from fastapi import FastAPI, Body
from nonebot.adapters.mirai2 import Bot, MessageChain, MessageSegment
from pydantic import BaseModel

global_config = get_driver().config
config = Config.parse_obj(global_config)

app: FastAPI = nonebot.get_app()


@app.post("/yuqueWebhook")
async def yuqueWebhook(body=Body(...)):
    logger.info(body)
    data: dict = body["data"]
    bot = get_bot()
    msg = "『茉莉开发组』团队公告\n"
    msg += f"成员【{data['user']['name']}】在仓库【{data['book']['name']}】:\n"
    path = f"https://jasmine-dev.yuque.com/{data['path']}"
    if data['publish']:
        msg += f"发布了一篇新文档：{data['title']}\nurl：{path}"
    else:
        if data['action_type'] == "update":
            msg += f"更新了文档状态：{data['title']}\nurl：{path}"
        elif data['action_type'] == "delete":
            msg += f"删除了文档：{data['title']}\nurl：{path}"
        else:
            msg += f"未知状态：{data['title']}\nurl：{path}"

    msg = msg.encode('utf-8').decode("utf-8")
    await bot.send_group_message(target=921454429, message_chain=MessageChain(MessageSegment.plain(msg)))
