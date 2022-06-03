import json
import requests
from nonebot import Bot, get_driver, logger
from nonebot.adapters.mirai2 import MessageChain, MessageSegment
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

# 判断数量是否超限


def judge_maxnum(num):
    if(num > config.maxnum):
        return False
    else:
        return True

# opt为0代表合并转发模式;1为“刷屏”模式


def judge_user_permission(qq: int, opt: int) -> bool:
    try:
        f = open(f"{config.conf_path}\\{qq}\\favorConf.json",
                 "r", encoding="utf-8")
    except:
        return False
    json_str = f.read()
    f.close()
    j = json.loads(json_str)
    if (opt == 0):
        if(j.__contains__("好感度") and j["好感度"] >= config.normal_favor_limit):
            return True
        else:
            return False
    elif(opt == 1):
        if(j.__contains__("好感度") and j["好感度"] >= config.boom_favor_limit):
            return True
        else:
            return False

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
        if(group == g):
            return True
    return False


def call_setu_api(num: int):
    # res = requests.get(
    #     f"https://api.lolicon.app/setu/v2?proxy=pixiv.runrab.workers.dev&num={num}").json()
    res = requests.get(
        f"https://api.lolicon.app/setu/v2?proxy=i.pixiv.cat&num={num}").json()
    if(res["error"] != ""):
        return False
    # 一条消息的消息链
    pic_list = MessageChain([])
    return_list = []
    # tags = ""

    # 提取返回json字段
    for data in res["data"]:
        title = data["title"]
        author = data["author"]
        # tag_cnt = 0
        # for tag in data["tags"]:
        #     tags = tags + f"| {tag}"
        #     tag_cnt = tag_cnt+1
        #     if(tag_cnt > 8):
        #         break
        pic_list.append(MessageSegment.plain(
            f"标题：{title}\n作者：{author}\n"))
        pic_list.append(MessageSegment.image(url=data["urls"]["original"]))
        return_list.append(pic_list)
        # tags = ""
        pic_list = MessageChain([])

    return return_list
