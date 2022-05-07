import json
from random import randint
from loguru import Message
from nonebot import Bot, get_driver, on_startswith
from nonebot.adapters.mirai2 import FriendMessage, MessageEvent, GroupMessage
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

#! 1298754454
trigger_1298754454_01 = on_startswith("...")
trigger_1298754454_02 = on_startswith("…")

@trigger_1298754454_01.handle()
@trigger_1298754454_02.handle()
async def reply_1298754454_01(event: FriendMessage):
    if(event.sender.id == 1298754454):
        await trigger_1298754454_01.finish(draw_reply(event.sender.id, "...", event), quote=event.source.id)

#! 4786515
trigger_4786515_01 = on_startswith("小姐")

@trigger_4786515_01.handle()
async def reply_4786515_01(event: MessageEvent):
    if(event.sender.id == 4786515):
        await trigger_4786515_01.finish(draw_reply(event.sender.id, "小姐", event), quote=event.source.id)

#! 839968342
trigger_839968342_01 = on_startswith("茉莉？")
trigger_839968342_02 = on_startswith("茉莉?")

@trigger_839968342_01.handle()
@trigger_839968342_02.handle()
async def reply_839968342_01(bot:Bot,event:MessageEvent):
    if event.sender.id == 839968342:
        await bot.send(draw_reply(event.sender.id,"茉莉？",event),quote=event.source.id)

def draw_reply(qq: int, trigger: str, event: MessageEvent):
    f = open(config.reply_path, "r", encoding="utf-8")
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
