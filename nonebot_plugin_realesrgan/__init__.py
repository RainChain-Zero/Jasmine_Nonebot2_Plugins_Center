from .utils import *
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment, Bot, Event
from nonebot.params import T_State, CommandArg
from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11.helpers import HandleCancellation
from json import loads
from nonebot import get_driver

try:
    api = loads(get_driver().config.json())["realesrgan_api"]
except:
    api = 'https://hf.space/embed/ppxxxg22/Real-ESRGAN/api/predict/'

real_esrgan = on_command(
    "超分重建", aliases={"real-esrgan", "超分辨率重建", "esrgan", "real_esrgan"}, priority=30
)


@real_esrgan.handle()
async def real_esrgan_handle_first(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    args: Message = CommandArg(),
):
    state['id'] = event.get_user_id()
    for seg in args:
        if seg.type == "text":
            state["mode"] = seg.data["text"].strip()
        if seg.type == "image":
            state['img'] = seg
            break


@real_esrgan.got("mode", prompt="请选择重建模式，输入anime或base", parameterless=[HandleCancellation("已取消")])
async def real_esrgan_get_mode(event: MessageEvent, state: T_State):
    mode = str(state["mode"]).strip()
    if mode not in ["anime", "base"]:
        await real_esrgan.reject('不存在的模式，请输入anime或base')


@real_esrgan.got("img", prompt="请输入待重建图像哦~注意，由于算力限制，不完全的模型对较大的图无法得到满意的效果", parameterless=[HandleCancellation("已取消")])
async def real_esrgan_handle_img(event: MessageEvent, state: T_State):
    # 先拿到需要转换的图
    for seg in state["img"]:
        if seg.type == "image":
            img = await get_img(seg.data["url"])
            break
    else:
        await real_esrgan.finish(Message(f"[CQ:at,qq={state['id']}]并不是图哦？"))
    # 下面来处理图片
    await real_esrgan.send(Message(f"茉莉正在处理图片，请稍后..."))
    try:
        json_data = img_encode_to_json(img, state['mode'])  # 先获取图片并进行编码
        if json_data is None:
            await real_esrgan.finish(Message(f"[CQ:at,qq={state['id']}]图片上传失败，请稍后再试"))
        result = await get_result(json_data, api=api)  # 然后进行超分辨率重建
        if result is None:
            await real_esrgan.finish(Message(f"[CQ:at,qq={state['id']}]图片解析失败，请向管理员报告——"))
        img = img_decode_from_json(result)  # 获取重建后图片并进行解码发送
        await real_esrgan.finish(MessageSegment.image(img))
    except Exception as e:
        ...
        # print('错误类型是', e.__class__.__name__)
        # print('错误明细是', e)
