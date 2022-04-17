import json
from random import randint
from nonebot import Bot, get_driver, on_startswith
from nonebot.adapters.mirai2 import FriendMessage, MessageEvent, GroupMessage
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)


yuki_trigger_01 = on_startswith("...")


@yuki_trigger_01.handle()
async def yuki_reply_01(event: FriendMessage):
    if(event.sender.id == 1298754454):
        await yuki_trigger_01.finish(draw_reply(event.sender.id, "...", event), quote=event.source.id)


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
