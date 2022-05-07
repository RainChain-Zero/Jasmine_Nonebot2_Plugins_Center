
from nonebot import get_driver, on_command, on_startswith
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message,PrivateMessageEvent
from nonebot.adapters.mirai2 import FriendMessage,Bot,GroupMessage
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)



yuki_01=on_command("test")

@yuki_01.handle()
async def Yuki (bot:Bot,event:GroupMessage):
    if(event.sender.id==3032902237):
        info = await bot.member_pro_file(target=event.sender.group.id,member_id=event.sender.id)
        info = await bot.friend_pro_file(target=event.sender.id)
        await yuki_01.finish("OK")
