from .config import Config
from .utils import Command
from .data_source import commands
from .depends import regex, split_msg
import base64
import json
from io import BytesIO
from typing import Union

from nonebot import get_driver, logger, on_message
from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot import on_command, require, on_regex
from nonebot.adapters.mirai2 import MessageSegment, MessageEvent

from ..utils.data import read_favor

# require("nonebot_plugin_imageutils")


global_config = get_driver().config
config = Config.parse_obj(global_config)


def create_matchers():
    def handler(command: Command) -> T_Handler:
        async def handle(
            event: MessageEvent, matcher: Matcher, res: Union[str, BytesIO] = Depends(command.func)
        ):
            if read_favor(event.sender.id) < 500:
                await matcher.finish("『×条件未满足』此功能要求好感度≥500")
            if isinstance(res, str):
                await matcher.finish(res)
            await matcher.finish(MessageSegment.image(base64=base64.b64encode(res.getvalue()).decode('utf-8')))

        return handle

    for command in commands:
        on_message(
            regex(command.pattern),
            block=False,
            priority=12,
        ).append_handler(handler(command), parameterless=[split_msg()])


create_matchers()
