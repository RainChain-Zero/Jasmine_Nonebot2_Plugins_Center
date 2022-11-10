from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.helpers import extract_image_urls
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import Arg
from nonebot.typing import T_State

from .cartoon import cartonization
from ..utils.data import read_favor
cartoonize = on_command("卡通化", aliases={"二次元化"})


@cartoonize.handle()
async def image_analysis(event: MessageEvent, matcher: Matcher):
    if read_favor(event.user_id) < 500:
        await cartoonize.finish("此功能需要好感度≥500哦")
    message = reply.message if (reply := event.reply) else event.message
    if imgs := message["image"]:
        matcher.set_arg("imgs", imgs)


@cartoonize.got("imgs", prompt="请发送需要二次元化的图片")
async def get_image(state: T_State, imgs: Message = Arg()):
    urls = extract_image_urls(imgs)
    if not urls:
        await cartoonize.reject("当前消息中没有检测到图片")
    state["urls"] = urls


@cartoonize.handle()
async def analysis_handle(state: T_State):
    await cartoonize.send("正在执行二次元化处理，请稍后...")
    try:
        image = await cartonization(state["urls"][0])
    except Exception as e:
        logger.opt(exception=e).error("转换图像失败")
        await cartoonize.finish("图片二次元化失败，请稍后再试", reply_message=True)
    await cartoonize.finish(MessageSegment.image(image), reply_message=True)
