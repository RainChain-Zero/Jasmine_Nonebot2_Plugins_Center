from nonebot import on_fullmatch, on_startswith
from nonebot.adapters.onebot.v11 import MessageEvent, Message, Bot, MessageSegment
from nonebot.typing import T_State
from nonebot.params import State, Arg, EventPlainText
import re
import time
from .apis import *
from ..utils.message import *
from ..utils.download import download_pic
from .config import Config
global_config = get_driver().config
config = Config.parse_obj(global_config)

get_truth_matcher = on_fullmatch('.q')
add_truth_matcher = on_startswith('.add q')
clear_truth_answered_matcher = on_fullmatch('.clear q')
get_truth_history_matcher = on_startswith('.get q')


@get_truth_matcher.handle()
async def get_truth_handle(event: MessageEvent, state: T_State = State()):
    truth = await get_truth(str(event.sender.user_id))
    if truth:
        state['id'] = truth['id']
        await get_truth_matcher.send(f"{truth['id']}\n{truth['question']}")
    else:
        await get_truth_matcher.finish(MessageSegment.reply(event.message_id)+"获取问题失败，你可能已经回答完了所有问题，请使用.clear q重置")


@get_truth_matcher.got('answer')
async def get_truth_got(bot: Bot, event: MessageEvent, message: Message = Arg('answer'), state: T_State = State()):
    answer_all: str = state.get('answer_all', '')
    if not message:
        message = []
    if message.extract_plain_text().startswith('end'):
        if not answer_all:
            await get_truth_matcher.finish(f'嗯嗯！感谢{event.sender.nickname}的精彩回答！')
        if await answer_truth(str(event.sender.user_id), state['id'], answer_all):
            await get_truth_matcher.finish(f'嗯嗯！感谢{event.sender.nickname}的精彩回答！')
        else:
            await get_truth_matcher.finish('记录回答失败，请联系管理员')
    for msg in message:
        if msg.type == 'text':
            answer_all += msg.data['text']
        elif msg.type == 'at':
            qq = msg.data.get('qq', '')
            user_info = await bot.get_stranger_info(user_id=int(qq))
            answer_all += f'@{user_info["nickname"]} '
        elif msg.type == 'image':
            # 下载图片到本地
            try:
                pic_uid = await download_pic(msg.data['url'], config.truth_pic_path)
            except Exception as e:
                logger.error(e)
                await get_truth_matcher.finish('警告：图片下载失败，已停止对此问题的记录')
            # 用[[path]]代替图片
            answer_all += f'[[{pic_uid}]]'
    # 用{{end}}分割不同条消息
    answer_all += r'{{end}}'
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
    if not history:
        await get_truth_history_matcher.finish('你在这个问题上还没有回答记录哦~')
    msgs = []
    for h in history:

        msg: str = h['answer'].strip(r'{{end}}')
        if not msg:
            continue
        msgs.append(time.strftime(r'%Y-%m-%d %H:%M:%S',
                                  time.gmtime(h['timeStamp']//1000)))
        # 分割不同条消息
        msg = msg.split(r'{{end}}')
        for msg_seg in msg:
            # 寻找[[和]]的起始位置
            pic_begin = msg_seg.find(r'[[')
            pic_end = msg_seg.find(r']]')
            if pic_begin != -1 and pic_end != -1:
                # 图片路径
                pic_uid = msg_seg[pic_begin+2:pic_end]
                pic_bytes = open(config.truth_pic_path+pic_uid,'rb').read()
                msgs.append(
                    Message([msg_seg[:pic_begin],
                             MessageSegment.image(
                                 pic_bytes),
                             msg_seg[pic_end+2:]]))
            else:
                msgs.append(msg_seg)
    if not msgs:
        await get_truth_history_matcher.finish('你在这个问题上还没有回答记录哦~')

    await send_forward_msg(bot, event, event.sender.nickname, event.sender.user_id, msgs)
