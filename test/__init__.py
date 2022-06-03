from email.mime import base
from io import BytesIO
from nonebot import get_driver, logger, on_command, on_startswith
from nonebot.adapters.mirai2 import FriendMessage, Bot, GroupMessage, MessageEvent,MessageSegment
from .config import Config
import base64
from nonebot_plugin_imageutils import BuildImage,Text2Image
global_config = get_driver().config
config = Config.parse_obj(global_config)

test_01 = on_command("t")

@test_01.handle()
async def test(bot: Bot, event: GroupMessage):
    img = Text2Image.from_text("文字转图片测试", 50).to_image()
    output_buffer = BytesIO()
    img.save(output_buffer,format='png')

    await test_01.finish(MessageSegment.image(base64=base64.b64encode(output_buffer.getvalue()).decode('utf-8')))