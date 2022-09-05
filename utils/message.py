from nonebot.adapters.mirai2 import Bot,MessageSegment

async def build_forward_pic_message(bot: Bot, img_url: list):
    node_list = []
    for img in img_url:
        data = {
            "senderId": bot.self_id,
            "time": 0,
            "senderName": "茉莉",
            "messageChain": [MessageSegment.image(url=img)],
            "messageId": None
        }
        node_list.append(data)
    return node_list
