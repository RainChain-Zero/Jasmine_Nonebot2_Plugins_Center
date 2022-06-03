import shlex
from io import BytesIO
from typing import List, Optional
from nonebot import logger
from nonebot.typing import T_State
from nonebot.params import State, Depends, RegexDict
from nonebot.adapters.mirai2 import (
    Bot,
    MessageChain,
    MessageSegment,
    MessageEvent,
    GroupMessage
)

from nonebot.adapters.onebot.v11 import unescape


from nonebot_plugin_imageutils import BuildImage

from .utils import UserInfo
from .download import download_url, download_avatar


USERS_KEY = "USERS"
SENDER_KEY = "SENDER"
ARGS_KEY = "ARGS"


def is_qq(msg: str):
    return msg.isdigit() and 11 >= len(msg) >= 5


def split_msg():
    def dependency(
        event: MessageEvent, state: T_State = State(), arg: dict = RegexDict()
    ):
        # msg = Message(arg["msg"])
        #! 获取消息链
        msg = event.get_message()
        users: List[UserInfo] = []
        args: List[str] = []
        for msg_seg in msg:
            if msg_seg.type == "At":
                users.append(
                    UserInfo(
                        qq=str(msg_seg.data.get("target", "")),
                        group=str(event.sender.group.id)
                        if isinstance(event, GroupMessage)
                        else "",
                    )
                )
            elif msg_seg.type == "Image":
                users.append(UserInfo(img_url=str(msg_seg.data.get("url", ""))))
            elif msg_seg.type == "Plain":
                raw_text = str(msg_seg)
                try:
                    texts = shlex.split(raw_text)
                except:
                    texts = raw_text.split()
                for text in texts:
                    if is_qq(text):
                        users.append(UserInfo(qq=text))
                    elif text == "自己":
                        users.append(
                            UserInfo(
                                qq=str(event.sender.id),
                                group=str(event.sender.group.id)
                                if isinstance(event, GroupMessage)
                                else "",
                            )
                        )
                    else:
                        text = unescape(text).strip()
                        if text:
                            args.append(text)
        #! 删除触发指令command
        args.remove(args[0])            
        sender = UserInfo(qq=str(event.sender.id))
        state[SENDER_KEY] = sender
        state[USERS_KEY] = users
        state[ARGS_KEY] = args

    return Depends(dependency)


async def get_user_info(bot: Bot, user: UserInfo):
    if not user.qq:
        return

    if user.group:
        info = await bot.member_profile(
            target=int(user.group), member_id=int(user.qq)
        )
        user.name = info.get("card", "") or info.get("nickname", "")
        user.gender = info.get("sex", "")
    else:
        info = await bot.friend_profile(target=int(user.qq))
        user.name = info.get("nickname", "")
        user.gender = info.get("sex", "")

async def download_image(user: UserInfo):
    img = None
    if user.qq:
        img = await download_avatar(user.qq)
    elif user.img_url:
        img = await download_url(user.img_url)

    if img:
        user.img = BuildImage.open(BytesIO(img))


def Users(min_num: int = 1, max_num: int = 1):
    async def dependency(bot: Bot, state: T_State = State()):
        users: List[UserInfo] = state[USERS_KEY]
        if len(users) > max_num or len(users) < min_num:
            return

        for user in users:
            await get_user_info(bot, user)
            await download_image(user)
        return users

    return Depends(dependency)


def User():
    async def dependency(users= Users()):
        if users:
            return users[0]

    return Depends(dependency)


def UserImgs(min_num: int = 1, max_num: int = 1):
    async def dependency(state: T_State = State()):
        users: List[UserInfo] = state[USERS_KEY]
        if len(users) > max_num or len(users) < min_num:
            return

        for user in users:
            await download_image(user)
        return [user.img for user in users]

    return Depends(dependency)


def UserImg():
    async def dependency(imgs: List[BuildImage] = UserImgs()):
        if imgs:
            return imgs[0]

    return Depends(dependency)


def Sender():
    async def dependency(bot: Bot, state: T_State = State()):
        sender: UserInfo = state[SENDER_KEY]
        await get_user_info(bot, sender)
        await download_image(sender)
        return sender

    return Depends(dependency)


def SenderImg():
    async def dependency(state: T_State = State()):
        sender: UserInfo = state[SENDER_KEY]
        await download_image(sender)
        return sender.img

    return Depends(dependency)


def Args(min_num: int = 1, max_num: int = 1):
    async def dependency(state: T_State = State()):
        args: List[str] = state[ARGS_KEY]
        if len(args) > max_num or len(args) < min_num:
            return
        return args

    return Depends(dependency)


def RegexArg(key: str):
    async def dependency(arg: dict = RegexDict()):
        return arg.get(key, None)

    return Depends(dependency)


def Arg(possible_values: List[str] = []):
    async def dependency(args: List[str] = Args(0, 1)):
        if args:
            arg = args[0]
            if possible_values and arg not in possible_values:
                return
            return arg
        else:
            return ""

    return Depends(dependency)


def NoArg():
    async def dependency(args: List[str] = Args(0, 0)):
        return

    return Depends(dependency)
