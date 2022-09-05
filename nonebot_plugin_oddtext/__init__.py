import traceback
from nonebot import on_command
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.adapters.mirai2 import MessageChain
from nonebot.typing import T_Handler
from nonebot.params import CommandArg
from nonebot.log import default_format
from loguru import logger as logger_
from .data_source import commands, Command


def create_matchers():
    def create_handler(command: Command) -> T_Handler:
        async def handler(matcher: Matcher, msg: MessageChain = CommandArg()):
            text = msg.extract_plain_text().strip()
            if not text:
                matcher.block = False
                await matcher.finish()
            try:
                res = command.func(text)
            except:
                logger.warning(traceback.format_exc())
                await matcher.finish("有哪里出错了，请稍后再试吧~")
            await matcher.finish(res)

        return handler

    for command in commands:
        on_command(
            command.keywords[0], aliases=set(command.keywords), block=True, priority=13
        ).append_handler(create_handler(command))


create_matchers()
