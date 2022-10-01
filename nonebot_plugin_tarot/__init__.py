
from email import message
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, PrivateMessageEvent, GroupMessageEvent, Message, MessageSegment
from typing import List

from .data_source import Cards, meanings, global_config

from ..utils.message import send_forward_msg

if not hasattr(global_config, "nickname"):
    NICKNAME = "Bot"
    raise Exception("Bot'd better have a nickname maybe.")
else:
    _NICKNAME = global_config.nickname
    if len(list(_NICKNAME)) > 0:
        NICKNAME = list(_NICKNAME)[0]
    else:
        NICKNAME = "Bot"

__tarot_vsrsion__ = "v0.2.5"
plugin_notes = f'''
塔罗牌 {__tarot_vsrsion__}
[塔罗牌] 得到单张塔罗牌回应
[占卜]  全套占卜'''.strip()

plugin_help = on_command("塔罗牌帮助", priority=6, block=True)
tarot = on_command("塔罗牌", priority=6, block=True)
divine = on_command("占卜", priority=6, block=True)


@plugin_help.handle()
async def show_help(bot: Bot, event: Event):
    await plugin_help.finish(plugin_notes)


@tarot.handle()
async def _(bot: Bot, event: Event):
    card = Cards(1)
    card_key, card_value, image_file = card.reveal()
    if isinstance(event, GroupMessageEvent):
        msg = MessageSegment.text(
            f"『{card_key}』\n{card_value}\n") + MessageSegment.image(image_file)
        await tarot.finish(message=msg, at_sender=True)
    else:
        msg = MessageSegment.text(
            f"『{card_key}』\n{card_value}\n") + MessageSegment.image(image_file)
        await tarot.finish(message=msg, at_sender=False)


@divine.handle()
async def _(bot: Bot, event: Event):
    cards = Cards(4)
    # chain = {
    #     "nodeList": [],
    # }
    chain = []
    for count in range(4):
        card_key, card_value, image_file = cards.reveal()
        meaning_key = list(meanings.keys())[count]
        meaning_value = meanings[meaning_key]

        text = meaning_key + "，" + meaning_value + \
            "\n" + "『"+card_key+"』" + "，" + card_value + "\n"
        msg = MessageSegment.text(
            text) + MessageSegment.image(image_file)
        chain.append(msg)
    await send_forward_msg(bot, event, '茉莉', bot.self_id, chain)
