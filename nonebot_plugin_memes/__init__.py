import base64
import shlex
import traceback
from nonebot import on_command, on_regex
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.params import CommandArg
from nonebot.adapters.mirai2 import MessageChain, MessageSegment, MessageEvent, FriendMessage

from nonebot.adapters.onebot.v11 import unescape
from nonebot.log import logger

from .models import NormalMeme
from .download import DownloadError
from .utils import help_image, judge_user_permission
from .normal_meme import normal_memes
from .gif_subtitle_meme import gif_subtitle_memes

from ..utils.data import read_favor

__help__plugin_name__ = "memes"
__des__ = "表情包制作"
__cmd__ = "发送“表情包制作”查看表情包列表"
__short_cmd__ = __cmd__
__example__ = """
鲁迅说 我没说过这句话
王境泽 我就是饿死 死外边 不会吃你们一点东西 真香
""".strip()
__usage__ = f"{__des__}\n\nUsage:\n{__cmd__}\n\nExamples:\n{__example__}"


help_cmd = on_command("表情包制作", block=True, priority=12)

memes = normal_memes + gif_subtitle_memes


@help_cmd.handle()
async def _():
    img = await help_image(memes)
    if img:
        await help_cmd.finish(MessageSegment.image(base64=base64.b64encode(img.getvalue()).decode('utf8')))


async def handle(matcher: Matcher, meme: NormalMeme, text: str):
    arg_num = meme.arg_num
    if arg_num == 1:
        texts = [text]
    else:
        try:
            texts = shlex.split(text)
        except:
            await matcher.finish(f"『×Error』参数解析错误!若包含特殊符号请转义哦~")

    if len(texts) < arg_num:
        await matcher.finish(f"『×参数错误』该表情包需要输入用空格隔开的{arg_num}段文字哦~")
    elif len(texts) > arg_num:
        await matcher.finish(f"『×参数错误』需要输入用空格隔开的{arg_num}段文字，若一段文字中包含空格请加引号~如\"就像这样 加双引号\"")

    try:
        res = await meme.func(texts)
    except DownloadError:
        logger.warning(traceback.format_exc())
        await matcher.finish("『×Error』资源下载出错啦——稍后再试试吧~")
    except:
        logger.warning(traceback.format_exc())
        await matcher.finish("『×Error』有些地方出错了诶...稍后再试吧")

    if isinstance(res, str):
        await matcher.finish(res)
    else:
        await matcher.finish(MessageSegment.image(base64=base64.b64encode(res.getvalue()).decode('utf8')))


def create_matchers():
    def create_handler(meme: NormalMeme) -> T_Handler:
        async def handler(event: MessageEvent, matcher: Matcher, msg: MessageChain = CommandArg()):
            text = unescape(msg.extract_plain_text()).strip()
            if (not text):
                await matcher.finish()
            else:
                if(read_favor(event.sender.id) >= 500):
                    await handle(matcher, meme, text)
                else:
                    await matcher.finish("『×条件未满足』当前功能需要好感度≥500")

        return handler

    for meme in memes:
        on_command(
            meme.keywords[0], aliases=set(meme.keywords), block=True, priority=13
        ).append_handler(create_handler(meme))


create_matchers()


#! 群聊中才可使用的功能

ph_handle = on_command("ph")
bwc_handle = on_command("bwc")
five_k_handle = on_command("5000兆")
zero_handle = on_regex("^/\\d+%")


@ph_handle.handle()
@bwc_handle.handle()
@five_k_handle.handle()
@zero_handle.handle()
async def friend_handle(event: FriendMessage, matcher: Matcher):
    await matcher.finish("『×Error』/ph /bwc /5000兆 /0% 这几个生成图片的指令暂时只能在群聊中进行呢")
