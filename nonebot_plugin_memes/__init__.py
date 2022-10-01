from .utils import Meme, help_image
from .data_source import memes
from .depends import regex
from io import BytesIO
from typing import Union
from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message, require
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent
from ..utils.data import read_favor

require("nonebot_plugin_imageutils")


help_cmd = on_command("表情包制作", block=True, priority=12)


def create_matchers():
    def handler(meme: Meme) -> T_Handler:
        async def handle(
            event: MessageEvent, matcher: Matcher, res: Union[str, BytesIO] = Depends(meme.func)
        ):
            if read_favor(event.sender.user_id) < 500:
                matcher.finish('茉莉的此项功能需要好感度≥500哦~')
            matcher.stop_propagation()
            if isinstance(res, str):
                await matcher.finish(res)
            await matcher.finish(MessageSegment.image(res))

        return handle

    for meme in memes:
        on_message(
            regex(meme.pattern),
            block=False,
            priority=12,
        ).append_handler(handler(meme))


create_matchers()
