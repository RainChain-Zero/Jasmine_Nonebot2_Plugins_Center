from nonebot import logger, on_command
from nonebot.adapters.mirai2 import Bot, MessageEvent, GroupMessage, FriendMessage, MessageChain, MessageSegment
from nonebot.matcher import Matcher

from .saucenao import saucenao_search


engine_dic = {"saucenao": saucenao_search}

saucenao_command = on_command("saucenao搜图")

@saucenao_command.handle()
async def pic_search(bot:Bot,event:MessageEvent,matcher:Matcher):
    # 提取图片
    try:
        img_url = event.get_message()["Image", 0].data["url"]
    except:
        await matcher.finish(f"『×Error』当前消息中没有图片哦~")

    # 匹配搜索引擎
    message = event.get_plaintext()
    engine = message[1:message.index("搜")].lower()

    await bot.send(event=event, message=f"『◎请稍后』茉莉正在处理图片...当前引擎{engine}")

    try:
        nodelist = await engine_dic[engine](bot, img_url)
    except:
        logger.error(f"{engine}搜图失败！")
        await matcher.finish(message=f"『×Error』{engine}搜图出错，请尝试更换引擎或稍后再试")

    if isinstance(event, GroupMessage):
        await bot.send_group_message(target=event.sender.group.id, message_chain=[{"type": "Forward", "nodeList": nodelist}])
    elif isinstance(event, FriendMessage):
        await bot.send_friend_message(target=event.sender.id, message_chain=[{"type": "Forward", "nodeList": nodelist}])