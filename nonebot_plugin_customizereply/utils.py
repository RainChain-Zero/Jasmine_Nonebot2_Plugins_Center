# 普遍性触发
import json
from random import randint
from .config import Config
from nonebot import get_driver, logger
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent

global_config = get_driver().config
config = Config.parse_obj(global_config)

# 普遍触发


def draw_normal_reply(level: int, trigger: str, event: MessageEvent):
    try:
        f = open(config.reply_path, "r", encoding="utf-8")
    except IOError:
        logger.error("找不到定制reply的json文件")
        return "数据读取失败，请联系维护人员"
    j = f.read()
    f.close()
    reply = json.loads(j)
    reply_list = reply["0"][trigger][str(level)]
    name = event.sender.nickname if isinstance(
        event, PrivateMessageEvent) else event.sender.nickname
    return reply_list[randint(0, len(reply_list)-1)].replace("{nick}", name)

# 指定人触发


def draw_special_reply(qq: int, trigger: str, event: MessageEvent):
    try:
        f = open(config.reply_path, "r", encoding="utf-8")
    except IOError:
        logger.error("找不到定制reply的json文件")
        return "数据读取失败，请联系维护人员"

    j = f.read()
    f.close()
    reply = json.loads(j)
    res_list = reply[str(qq)][trigger]
    name = ""
    if (isinstance(event, PrivateMessageEvent)):
        name = event.sender.nickname
    elif (isinstance(event, GroupMessageEvent)):
        name = event.sender.card
    return res_list[randint(0, len(res_list)-1)].replace("{nick}", name)
