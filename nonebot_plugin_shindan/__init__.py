import base64
import json
import re
import traceback
from nonebot.rule import Rule
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot import on_command, on_message
from nonebot.params import  EventMessage, EventPlainText, State
from nonebot.adapters.mirai2 import (
    Bot,
    MessageEvent,
    MessageChain,
    MessageSegment,
    GroupMessage,
    FriendMessage
)

from .shindan_list import get_shindan_list
from .shindanmaker import make_shindan

cmd_ls = on_command('占卜列表', aliases={'可用占卜'}, block=True, priority=8)

@cmd_ls.handle()
async def _():
    sd_list = get_shindan_list()

    if not sd_list:
        await cmd_ls.finish('『×Error』还未添加任何占卜')

    await cmd_ls.finish(
        f'可用占卜：\n'
        + '\n'.join([f"{s['command']}（{s['title']}）" for s in sd_list.values()])
    )

def sd_handler() -> Rule:
    async def handle(
        bot: Bot,
        event: MessageEvent,
        msg: MessageChain = EventMessage(),
        msg_text: str = EventPlainText(),
        state: T_State = State(),
    ) -> bool:
        async def get_name(command: str) -> str:
            name = msg_text[len(command) :].strip()
            if not name:
                if isinstance(event,GroupMessage):
                    name = event.sender.name
                elif isinstance(event,FriendMessage):
                    name = event.sender.nickname
            return name

        sd_list = get_shindan_list()
        sd_list = sorted(
            sd_list.items(), reverse=True, key=lambda items: items[1]['command']
        )
        for id, s in sd_list:
            command = s['command']
            if msg_text.startswith(command):
                name = await get_name(command)
                state['id'] = id
                state['name'] = name
                state['mode'] = s.get('mode', 'image')
                return True
        return False

    return Rule(handle)


sd_matcher = on_message(sd_handler(), priority=9)


@sd_matcher.handle()
async def _(event:MessageEvent,state: T_State = State()):
    if not judge_user_permission(event.sender.id):
        await sd_matcher.finish('『×条件未满足』此功能要求好感度≥500')
    id = state.get('id')
    name = state.get('name')
    mode = state.get('mode')
    try:
        res = await make_shindan(id, name, mode)
    except:
        logger.warning(traceback.format_exc())
        await sd_matcher.finish('『×Error』有哪里不对了...请稍后再试')

    if isinstance(res, str):
        img_pattern = r'((?:http|https)://\S+\.(?:jpg|jpeg|png|gif|bmp|webp))'
        message = MessageChain([])
        msgs = re.split(img_pattern, res)
        for msg in msgs:
            message.append(
                MessageSegment.image(url=msg) if re.match(img_pattern, msg) else msg
            )
        await sd_matcher.finish(message)
    elif isinstance(res, bytes):
        await sd_matcher.finish(MessageSegment.image(base64=base64.b64encode(res).decode('utf8')))


def judge_user_permission(qq: int) -> bool:
    try:
        f = open(f"/home/mirai/Dice3349795206/UserConfDir/{qq}/favorConf.json",
                 "r", encoding="utf-8")
    except:
        return False
    json_str = f.read()
    f.close()
    j = json.loads(json_str)
    if(j.__contains__("好感度") and j["好感度"] >= 500):
        return True
    else:
        return False