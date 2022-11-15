from nonebot import on_fullmatch, on_startswith
from nonebot.adapters.onebot.v11 import MessageEvent, Message, Bot
from nonebot.typing import T_State
from nonebot.params import State, ArgPlainText, EventPlainText
import re
import time
from .apis import *
from ..utils.message import *

get_truth_matcher = on_fullmatch('.q')
add_truth_matcher = on_startswith('.add q')
clear_truth_answered_matcher = on_fullmatch('.clear q')
get_truth_history_matcher = on_startswith('.get q')


@get_truth_matcher.handle()
async def get_truth_handle(event: MessageEvent, state: T_State = State()):
    truth = await get_truth(str(event.sender.user_id))
    if truth:
        state['id'] = truth['id']
        await get_truth_matcher.send(f"{truth['id']}\n{truth['question']}", reply_message=True)
    else:
        await get_truth_matcher.finish("获取问题失败，你可能已经回答完了所有问题，请使用.clear q重置", reply_message=True)


@get_truth_matcher.got('answer')
async def get_truth_got(event: MessageEvent, message: str = ArgPlainText('answer'), state: T_State = State()):
    answer_all = state.get('answer_all', '')
    if not message:
        message = ''
    if message.startswith('end'):
        if not answer_all:
            await get_truth_matcher.finish(f'嗯嗯！感谢{event.sender.nickname}的精彩回答！')
        if await answer_truth(str(event.sender.user_id), state['id'], answer_all):
            await get_truth_matcher.finish(f'嗯嗯！感谢{event.sender.nickname}的精彩回答！')
        else:
            await get_truth_matcher.finish('记录回答失败，请联系管理员')
    # 用{{end}}分割不同条消息
    answer_all += message+r'{{end}}'
    state['answer_all'] = answer_all
    await get_truth_matcher.reject()


@add_truth_matcher.handle()
async def add_truth_handle(event: MessageEvent, message: str = EventPlainText()):
    truth = message[6:].strip()
    if not truth:
        await add_truth_matcher.finish('要添加的问题不能为空哦？')
    if await add_truth(f'{event.sender.nickname}({event.sender.user_id})', truth):
        await add_truth_matcher.finish('问题添加成功！')
    else:
        await add_truth_matcher.finish('问题添加失败，请联系管理员')


@clear_truth_answered_matcher.handle()
async def clear_truth_answered_handle(event: MessageEvent):
    if await clear_truth_answered(str(event.sender.user_id)):
        await clear_truth_answered_matcher.finish('已清除回答过的问题记录，现在可以被重新抽取')
    else:
        await clear_truth_answered_matcher.finish('清除失败！请联系管理员')


@get_truth_history_matcher.handle()
async def get_truth_history_handle(bot: Bot, event: MessageEvent, message: str = EventPlainText()):
    id = re.findall(r'\d+', message)
    if not id:
        await get_truth_history_matcher.finish('请输入问题编号')
    history = await get_truth_history(str(event.sender.user_id), int(id[0]))
    msgs = Message()
    for h in history:

        msg = h['answer'].strip(r'{{end}}')
        if not msg:
            continue
        msgs.append(time.strftime(r'%Y-%m-%d %H:%M:%S',
                                  time.gmtime(h['timeStamp']//1000)))
        msg = msg.split(r'{{end}}')
        for text in msg:
            msgs.append(text)
    if not msgs:
        await get_truth_history_matcher.finish('你在这个问题上还没有回答记录哦~')

    await send_forward_msg(bot, event, event.sender.nickname, event.sender.user_id, msgs)
