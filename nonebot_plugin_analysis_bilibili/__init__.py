import re
from .analysis_bilibili import b23_extract, bili_keyword
from nonebot import get_driver, on_regex
from nonebot.adapters.mirai2 import MessageEvent,GroupMessage,FriendMessage
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

analysis_bili = on_regex(
    r"(b23.tv)|(bili(22|23|33|2233).cn)|(.bilibili.com)|(^(av|cv)(\d+))|(^BV([a-zA-Z0-9]{10})+)|"
    r"(\[\[QQ小程序\]哔哩哔哩\])|(QQ小程序&amp;#93;哔哩哔哩)|(QQ小程序&#93;哔哩哔哩)",
    flags=re.I,
)


@analysis_bili.handle()
async def analysis_main(event: MessageEvent) -> None:
    #! 跳过不解析的群
    if isinstance(event,GroupMessage) and event.sender.group.id in config.group_ignore:
        await analysis_bili.finish()

    text = str(event.get_message()).strip()
    if re.search(r"(b23.tv)|(bili(22|23|33|2233).cn)", text, re.I):
        # 提前处理短链接，避免解析到其他的
        text = await b23_extract(text)
    if isinstance(event,GroupMessage):
        group_id = event.sender.id
    elif isinstance(event,FriendMessage):
        group_id = event.sender.id
    else:
        group_id = None
    msg = await bili_keyword(group_id, text)
    if msg:
        try:
            await analysis_bili.send(msg)
        except:
            await analysis_bili.send("茉莉检测到风控风险，正在去除简介...")
            msg = re.sub(r"简介.*", "", msg)
            await analysis_bili.send(msg)
