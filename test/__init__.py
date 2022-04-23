from operator import imod
from nonebot import Bot, get_driver, on_command, on_startswith
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message,PrivateMessageEvent
from nonebot.adapters.mirai2 import FriendMessage
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)



yuki_01=on_command("测试")

@yuki_01.handle()
async def Yuki (bot:Bot,event:FriendMessage):
    if(event.sender.id==3032902237):
        await yuki_01.finish("OK")
