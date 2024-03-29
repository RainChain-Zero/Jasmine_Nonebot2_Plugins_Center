import base64

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, MessageEvent
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.log import logger

from .data_source import color_car, get_img, gray_car

mirage_tank = on_command(
    "幻影合成", aliases={"miragetank"}, priority=13
)


@mirage_tank.handle()
async def handle_first(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    args: Message = CommandArg(),
):
    images = []
    for seg in args:
        if seg.type == "text":
            state["mod"] = seg.data["text"].strip()
        elif seg.type == "image":
            images.append(seg)
    if len(images) >= 1:
        state["img1"] = images[0]
    if len(images) >= 2:
        state["img2"] = images[1]


@mirage_tank.got(
    "mod", prompt="『INFO』需要指定结果类型: gray | color")
async def get_mod(event: MessageEvent, state: T_State):
    mod = str(state["mod"]).strip()
    if mod not in ["gray", "color"]:
        await mirage_tank.reject('『INFO』需要在gray和color二选一，直接输入就好啦')


@mirage_tank.got(
    "img1", prompt="『INFO』请发送两张图哦，按表里顺序")
@mirage_tank.got("img2", prompt="『INFO』还需要一张里图哦~")
async def get_images(state: T_State):
    imgs = []
    mod = str(state["mod"])
    for seg in state["img1"] + state["img2"]:
        if seg.type != "image":
            await mirage_tank.reject("『ERROR』无法找到两张图片，不要逗我玩哦×")
        imgs.append(await get_img(seg.data["url"]))

    await mirage_tank.send("『INFO』茉莉开始合成幻影图...")

    res = None
    if mod == "gray":
        res = await gray_car(imgs[0], imgs[1])
    elif mod == "color":
        res = await color_car(imgs[0], imgs[1])
    if res:
        await mirage_tank.finish(MessageSegment.image(res))
