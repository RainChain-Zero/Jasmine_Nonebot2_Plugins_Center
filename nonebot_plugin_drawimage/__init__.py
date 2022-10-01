from nonebot import get_driver, on_command, logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.typing import T_State
from nonebot.params import State
from .config import Config

from ..utils.data import read_favor
from ..utils.message import *

# 引入作图api工具包
import wenxin_api
from wenxin_api.tasks.text_to_image import TextToImage

global_config = get_driver().config
config = Config.parse_obj(global_config)

# api key
wenxin_api.ak = config.api_key
wenxin_api.sk = config.secret_key

# 当前是否有处理任务
Working = False
# 作画风格
Style = ["古风", '油画', '水彩画', '卡通画', '二次元', '浮世绘',
         "蒸汽波艺术", "low poly", "像素风格", "概念艺术", "未来主义", "赛博朋克",
         "写实风格", "洛丽塔风格", "巴洛克风格", "超现实主义"]

draw_pic = on_command('作图')


@draw_pic.handle()
async def draw_pic_handle(bot: Bot, event: MessageEvent, state: T_State = State()):
    if read_favor(event.sender.user_id) < 3000:
        await draw_pic.finish("『×条件未满足』此功能要求好感度≥3000")
    if Working:
        await draw_pic.finish("『×当前有任务正在进行中』请稍后再试")
    des = event.get_plaintext()[4:].strip()
    if not des:
        await draw_pic.finish("『×参数错误』请输入正确的描述性文字\n[形容词] [主语] ，[细节设定]， [修饰语或者艺术家]")
    state['des'] = des


@draw_pic.got('style', prompt='请选择绘画风格，仅输入编号\n1.古风\n2.油画\n3.水彩画\n4.卡通画\n5.二次元\n6.浮世绘\n'
              '7.蒸汽波艺术\n8.low poly\n9.像素风格\n10.概念艺术\n11.未来主义\n12.赛博朋克\n13.写实风格\n14.洛丽塔风格\n15.巴洛克风格\n16.超现实主义')
async def draw_pic_got(bot: Bot, event: MessageEvent, state: T_State = State()):
    global Working
    index = str(state['style'])
    if not index.isdigit():
        await draw_pic.finish('『×参数错误』请输入正确的绘画风格编号')
    index = int(index)
    if index > len(Style) or index < 1:
        await draw_pic.reject('『×参数错误』编号超出范围，请重新输入')
    style = Style[index-1]
    # 开始作图
    await draw_pic.send('开始作图，请稍后...这可能需要一段时间...')
    Working = True
    try:
        rst = TextToImage.create(text=state['des'], style=str(style))
        msgs = [MessageSegment.image(await get_img(img_url))
                for img_url in rst['imgUrls']]
    except Exception as e:
        logger.error(e)
        Working = False
        await draw_pic.finish('『×作图失败』请检查文字是否符合要求或稍后再试')
    Working = False
    await send_forward_msg(bot, event, "茉莉", bot.self_id, msgs)
