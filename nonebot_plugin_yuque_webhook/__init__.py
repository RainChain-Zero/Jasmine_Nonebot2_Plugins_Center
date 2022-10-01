import json
from nonebot import get_driver, get_bot, logger
import nonebot
from .config import Config
from fastapi import FastAPI, Body
from nonebot.adapters.onebot.v11 import Bot

global_config = get_driver().config
config = Config.parse_obj(global_config)

app: FastAPI = nonebot.get_app()


@app.post("/yuqueWebhook")
async def yuqueWebhook(body=Body(...)):
    logger.info(body)
    data: dict = body["data"]
    bot: Bot = get_bot()
    msg = "『茉莉开发组』团队公告\n"
    msg += f"【{data['user']['name']}】在"
    path = f"https://jasmine-dev.yuque.com/{data['path']}"
    action_type = data["action_type"]
    if action_type == 'publish':
        msg += f"{data['book']['name']}中发布了一篇新文档【{data['title']}】\n"
    elif action_type == 'update':
        msg += f"{data['book']['name']}中更新了一篇文档【{data['title']}】\n"
    elif action_type == 'comment_create':
        msg += f"{data['commentable']['book']['name']}中的文档【{data['commentable']['title']}】新增了一条评论\n"
    elif action_type == 'new_review':
        msg += f"【{data['book']['name']}】中发起了一个评审\n"
    elif action_type == 'complete_review':
        msg += f"【{data['book']['name']}】中的评审已经完成\n"
    elif action_type == 'comment_reply_create':
        msg += f"{data['commentable']['book']['name']}中的文档【{data['commentable']['title']}】新增了一条回复评论\n"
    msg += f"目标url：{path}"

    msg = msg.encode('utf-8').decode("utf-8")
    await bot.send_group_msg(group_id=921454429, message=msg)
