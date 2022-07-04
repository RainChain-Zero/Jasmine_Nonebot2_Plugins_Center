import json
from .data_source import CaiyunAi, model_list,caiyun_config
from .config import Config
from nonebot_plugin_imageutils import text2image, BuildImage
import base64
import re
from typing import List, Union
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot import logger, on_command, require
from nonebot.params import CommandArg, ArgPlainText, State
from nonebot.adapters.mirai2 import (
    Bot,
    MessageEvent,
    GroupMessage,
    FriendMessage,
    MessageChain,
    MessageSegment,
)

require("nonebot_plugin_imageutils")


novel = on_command("续写", aliases={"彩云小梦"}, block=True, priority=12)


@novel.handle()
async def _(matcher: Matcher, msg: MessageChain = CommandArg()):
    content = msg.extract_plain_text().strip()
    if content:
        matcher.set_arg("content", msg)


@novel.got("content", prompt="请发送要续写的内容")
async def _(matcher: Matcher, content: str = ArgPlainText(), state: T_State = State()):
    matcher.set_arg("reply", MessageChain(
        [MessageSegment.plain(f"续写{content}")]))
    caiyunai = CaiyunAi()
    state["caiyunai"] = caiyunai


@novel.got("reply")
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State = State(),
    reply: str = ArgPlainText(),
):
    # 好感要求500
    if read_favor(event.sender.id)<500:
        await novel.finish("『WARNING』此功能要求好感度≥500哦")
    caiyunai: CaiyunAi = state["caiyunai"]
    if not reply.startswith("/"):
        reply = f"/{reply}"
    match_continue = re.match(r"/续写\s*(\S+.*)", reply, re.S)
    match_select = re.match(r"/选择分支\s*(\d+)", reply)
    match_model = re.match(r"/切换模型\s*(\S+)", reply)
    match_stop = re.match(r"/结束续写", reply)
    model_help = f"现在支持的模型：{'、'.join(list(model_list))}"
    if match_model:
        model = match_model.group(1).strip()
        if model not in model_list:
            await novel.reject(model_help)
        else:
            caiyunai.model = model
            await novel.reject(f"『SUCCESS』模型已切换为：{model}")
    elif match_continue:
        content = match_continue.group(1)
        caiyunai.content = content
    elif match_select:
        num = int(match_select.group(1))
        if num < 1 or num > len(caiyunai.contents):
            await novel.reject("『ERROR』请发送正确的编号哦~")
        caiyunai.select(num - 1)
    elif match_stop:
        await novel.finish("『INFO』续写已经结束啦~")
    else:
        await novel.reject()

    await novel.send("『INFO』茉莉正在生成文本...")
    err_msg = await caiyunai.next()
    if err_msg:
        await novel.finish(err_msg)
    nickname = model_list[caiyunai.model]["name"]
    help_msg = (
        "发送“/选择分支 编号”选择分支\n"
        "发送“/续写 内容”手动添加内容\n"
        "发送“/切换模型 名称”切换模型\n"
        f"{model_help}\n"
        "发送“/结束续写”结束续写"
    )
    msgs = [{
        "senderId": bot.self_id,
        "time": 0,
        "senderName": nickname,
        "messageChain": MessageChain([MessageSegment.plain(help_msg)]),
        "messageId": None
    }]
    result = BuildImage(
        text2image(caiyunai.result, padding=(20, 20), max_width=800)
    ).save_jpg()
    result = MessageChain([MessageSegment.image(
        base64=base64.b64encode(result.getvalue()).decode())])
    msgs = build_forward_message(bot, nickname, result, msgs)
    for i, content in enumerate(caiyunai.contents, start=1):
        msg_chain = MessageChain([MessageSegment.plain(f"{i}、\n{content}")])
        msgs = build_forward_message(bot, nickname, msg_chain, msgs)
    try:
        if isinstance(event, GroupMessage):
            await bot.send_group_message(target=event.sender.group.id, message_chain=[{"type": "Forward", "nodeList": msgs}])
        elif isinstance(event, FriendMessage):
            await bot.send_friend_message(target=event.sender.id, message_chain=[{"type": "Forward", "nodeList": msgs}])
    except:
        await novel.finish("『ERROR』消息发送失败，续写结束")
    await novel.reject()


def build_forward_message(bot: Bot, nickname: str, msg_chain: MessageChain, nodelist: List) -> List:
    data = {
        "senderId": bot.self_id,
        "time": 0,
        "senderName": nickname,
        "messageChain": msg_chain,
        "messageId": None
    }
    nodelist.append(data)
    return nodelist

def read_favor(qq: int) -> int:
    try:
        f = open(caiyun_config.favor_path+str(qq)+caiyun_config.favor_conf,
                 "r", encoding="utf-8")
    except:
        return 0
    json_str = f.read()
    f.close()
    j = json.loads(json_str)
    return j["好感度"] if j.__contains__("好感度") else 0