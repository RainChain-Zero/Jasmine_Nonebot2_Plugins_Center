from .config import Config
from .utils import Command
from .data_source import commands
from .depends import split_msg
import base64
import re
import json
from io import BytesIO
from typing import Union

from nonebot import get_driver, logger
from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot import on_command, require, on_regex
from nonebot.adapters.mirai2 import MessageSegment, MessageEvent

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
        start = "|".join(get_driver().config.command_start)
        regex = rf"^(?:{start})(?:{command.keyword})(?P<msg>.*)"
        on_regex(
            regex,
            flags=re.S,
            block=True,
            priority=12,
        ).append_handler(handler=handler(command), parameterless=[split_msg()])


create_matchers()


def read_favor(qq: int) -> int:
    try:
        f = open(config.favor_path+str(qq)+config.favor_conf,
                 "r", encoding="utf-8")
    except:
        return 0
    json_str = f.read()
    f.close()
    j = json.loads(json_str)
    return j["好感度"] if j.__contains__("好感度") else 0
