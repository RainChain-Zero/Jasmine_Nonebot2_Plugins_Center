# 普遍性触发
import json
from random import randint
from .config import Config
from nonebot import get_driver, logger
from nonebot.adapters.mirai2 import MessageEvent, FriendMessage, GroupMessage
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
        event, FriendMessage) else event.sender.name
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
    if(isinstance(event, FriendMessage)):
        name = event.sender.nickname
    elif(isinstance(event, GroupMessage)):
        name = event.sender.name
    return res_list[randint(0, len(res_list)-1)].replace("{nick}", name)


def read_favor(qq: int) -> int:
    try:
        f = open(config.favor_path+qq+config.favor_conf,
                 "r", encoding="utf-8")
    except:
        logger.info(f"用户{qq}好感配置文件不存在！返回默认值零")
        return 0
    json_str = f.read()
    f.close()
    j = json.loads(json_str)
    return j["好感度"] if j.__contains__("好感度") else 0