
from email.quoprimime import quote
from nonebot import Bot, on_message, on_regex, on_startswith
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, MessageEvent, GroupMessageEvent
from nonebot.matcher import Matcher
from .utils import draw_normal_reply, draw_special_reply

from ..utils.data import read_favor

#! 1298754454
trigger_1298754454_01 = on_startswith("...")
trigger_1298754454_02 = on_startswith("…")


@trigger_1298754454_01.handle()
@trigger_1298754454_02.handle()
async def reply_1298754454_01(event: PrivateMessageEvent):
    if(event.sender.user_id == 1298754454):
        await trigger_1298754454_01.finish(draw_special_reply(event.sender.user_id, "..."), reply_message=True)

#! 4786515
trigger_4786515_01 = on_startswith("小姐")
trigger_4786515_02 = on_startswith("茉莉看路灯")
trigger_4786515_03 = on_startswith("小姐我们回来了")


@trigger_4786515_01.handle()
async def reply_4786515_01(event: MessageEvent):
    if(event.sender.user_id == 4786515):
        await trigger_4786515_01.finish(draw_special_reply(event.sender.user_id, "小姐"), reply_message=True)


@trigger_4786515_02.handle()
async def reply_4786515_02(event: MessageEvent):
    if event.sender.user_id == 4786515:
        await trigger_4786515_02.finish(draw_special_reply(event.sender.user_id, "茉莉看路灯"), reply_message=True)


@trigger_4786515_03.handle()
async def reply_4786515_03(event: MessageEvent):
    if event.sender.user_id == 4786515:
        await trigger_4786515_03.finish(draw_special_reply(event.sender.user_id, "小姐我们回来了"), reply_message=True)

#! 839968342
trigger_839968342_01 = on_startswith("茉莉？")
trigger_839968342_02 = on_startswith("茉莉?")


@trigger_839968342_01.handle()
@trigger_839968342_02.handle()
async def reply_839968342_01(matcher: Matcher, bot: Bot, event: MessageEvent):
    if event.sender.user_id == 839968342:
        await matcher.finish(draw_special_reply(event.sender.user_id, "茉莉？"), reply_message=True)

#! 3449791431
trigger_3449791431_01 = on_regex("^呜呜呜")


@trigger_3449791431_01.handle()
async def reply_3449791431_01(bot: Bot, event: MessageEvent):
    level = 1
    favor = read_favor(event.sender.user_id)
    if favor > 500 and favor < 3000:
        level = 1
    elif favor >= 3000 and favor < 6500:
        level = 2
    elif favor >= 6500:
        level = 3
    await trigger_3449791431_01.finish(draw_normal_reply(level, "呜呜呜"), reply_message=True)

#! “茉莉”的回复
# trigger_moli = on_regex("^茉莉$")


# @trigger_moli.handle()
# async def reply_moli(bot: Bot, event: MessageEvent):
#     if event.sender.id in [2595928998, 751766424]:
#         await bot.send(event, draw_special_reply(event.sender.id, "茉莉", event), quote=event.source.id)
