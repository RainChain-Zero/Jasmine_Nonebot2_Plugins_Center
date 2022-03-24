import imp
from nonebot import get_driver, on_command
from nonebot.adapters.mirai2 import MessageEvent,GroupMessage,MessageChain,MessageSegment
from PIL import Image
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)


test=on_command("测试")

@test.handle()
async def _ (event:MessageEvent):
    msg=event.get_message()
    
    await test.finish(msg[1].data['url'])

