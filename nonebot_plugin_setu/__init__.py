import json
import re
import aiohttp
import asyncio
from nonebot import Bot, get_driver, logger, on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message, MessageSegment
from nonebot.params import CommandArg

from .config import Config

from .utils import call_moe_api, call_setu_api, get_pivix_pic, judge_group_permission, judge_maxnum

from ..utils.data import read_favor

global_config = get_driver().config
config = Config.parse_obj(global_config)

setu_normal = on_command("涩图")
setu_boom = on_command("涩图来")
offer_permission = on_command("授权涩图")
takeback_permission = on_command("收回涩图")
# 萌图
moe_command = on_command("萌图")

# "刷屏"涩图


@setu_boom.handle()
async def send_setu_boom(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext()
    try:
        num = int(re.compile(r"\d+").findall(msg)[0])
    except:
        num = 1
    if (not judge_maxnum(num)):
        await setu_boom.finish("『✖Error』一下太多对身体不好哦？")
    if (read_favor(event.sender.user_id) < 3000):
        await setu_boom.finish("『✖条件未满足』茉莉还不想给你看这些哦~(此功能好感要求>3000)")
    if (isinstance(event, GroupMessageEvent) and not judge_group_permission(event.group_id)):
        await setu_boom.finish("『✖群权限不足』茉莉并不觉得在这里这么做是安全的哦×(此功能需要向茉莉管理员申请许可)")

    messagechain_list = await call_setu_api(num)

    await setu_boom.finish(messagechain_list)
# 授权涩图


@offer_permission.handle()
async def offer_group_permission(event: MessageEvent):
    msg = event.get_plaintext()
    group = int(re.compile(r"\d+").findall(msg)[0])
    if (event.sender.user_id in config.admin_list):
        try:
            f = open(config.group_permission_path, "r", encoding="utf-8")
        except:
            logger.error("nonebot_plugin_setu:找不到群权限配置文件")
            await offer_permission.finish("『✖Error』找不到群权限配置文件")
        json_str = f.read()
        f.close()
        j = json.loads(json_str)
        j["group_list"].append(group)
        # 写入群权限配置文件
        f = open(config.group_permission_path, "w", encoding="utf-8")
        f.write(json.dumps(j))
        f.close()
        await offer_permission.finish(f"权限确认：已授予群{group}涩图权限")
    else:
        await offer_permission.finish("『✖权限不足』您没有执行此操作的权限")

# 收回涩图权限


@takeback_permission.handle()
async def takeback_group_permission(event: MessageEvent):
    msg = event.get_plaintext()
    group = int(re.compile(r"\d+").findall(msg)[0])
    if (event.sender.id in config.admin_list):
        try:
            f = open(config.group_permission_path, "r", encoding="utf-8")
        except:
            logger.error("nonebot_plugin_setu:找不到群权限配置文件")
            await takeback_permission.finish("『✖Error』找不到群权限配置文件")
        json_str = f.read()
        f.close()
        j = json.loads(json_str)
        j["group_list"].remove(group)
        # 写入群权限配置文件
        f = open(config.group_permission_path, "w", encoding="utf-8")
        f.write(json.dumps(j))
        f.close()
        await offer_permission.finish(f"权限确认：已收回群{group}涩图权限")
    else:
        await offer_permission.finish("『✖权限不足』您没有执行此操作的权限")


@moe_command.handle()
async def send_moe(event: MessageEvent, args: Message = CommandArg()):
    if (read_favor(event.sender.user_id) < 2500):
        await setu_boom.finish("『✖条件未满足』茉莉还不想给你看这些哦~(此功能好感要求>2500)")
    args = args.extract_plain_text().split()
    num = 1
    for i in range(len(args)):
        if args[i].isdigit():
            num = int(args[i])
            del args[i]
            break
    if (not judge_maxnum(num)):
        await setu_boom.finish(f"『✖Error』数量最多为{config.maxnum}张哦")
    async with aiohttp.ClientSession() as session:
        try:
            moe_list = await call_moe_api(num, args, session=session)
            corutine_list = []
            for moe in moe_list:
                corutine_list.append(get_pivix_pic(
                    r18=True if moe['nsfw'] == 2 else False, pid=moe['pid'], session=session))
            # 并发获取图片
            pic_list = await asyncio.gather(*corutine_list)
        except Exception as e:
            logger.error(f"nonebot_plugin_setu:获取萌图失败，{e}")
        else:
            msg = Message()
            for pic in pic_list:
                msg.extend(pic)
            await moe_command.finish(msg)
