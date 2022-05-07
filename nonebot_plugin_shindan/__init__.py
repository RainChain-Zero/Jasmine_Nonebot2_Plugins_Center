import base64
import re
import traceback
from nonebot.rule import Rule, to_me
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot import on_command, on_message
from nonebot.params import CommandArg, EventMessage, EventPlainText, State
from nonebot.adapters.mirai2 import (
    Bot,
    MessageEvent,
    MessageChain,
    MessageSegment,
)

from .shindan_list import get_shindan_list
from .shindanmaker import make_shindan, get_shindan_title

cmd_ls = on_command('占卜列表', aliases={'可用占卜'}, block=True, priority=8)

@cmd_ls.handle()
async def _():
    sd_list = get_shindan_list()

    if not sd_list:
        await cmd_ls.finish('『×Error』尚未添加任何占卜')

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
            # name = ''
            # for msg_seg in msg:
            #     if msg_seg.type == 'at':
            #         assert isinstance(event, GroupMessageEvent)
            #         info = await bot.get_group_member_info(
            #             group_id=event.group_id, user_id=msg_seg.data['qq']
            #         )
            #         name = info.get('card', '') or info.get('nickname', '')
            #         break
            # if not name:
            #     name = msg_text[len(command) :].strip()
            # if not name:
            #     name = event.sender.card or event.sender.nickname
            name = msg_text[len(command) :].strip()
            return name

        sd_list = get_shindan_list()
        sd_list = sorted(
            sd_list.items(), reverse=True, key=lambda items: items[1]['command']
        )
        for id, s in sd_list:
            command = s['command']
            if msg_text.startswith(f'/{command}'):
                name = await get_name(command)
                state['id'] = id
                state['name'] = name
                state['mode'] = s.get('mode', 'image')
                return True
        return False

    return Rule(handle)


sd_matcher = on_message(sd_handler(), priority=9)


@sd_matcher.handle()
async def _(state: T_State = State()):
    id = state.get('id')
    name = state.get('name')
    mode = state.get('mode')
    try:
        res = await make_shindan(id, name, mode)
    except:
        logger.warning(traceback.format_exc())
        await sd_matcher.finish('出错了，请稍后再试')

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
