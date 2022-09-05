from nonebot import get_driver, on_command, logger
from nonebot.adapters.mirai2 import Bot, MessageEvent, GroupMessage, FriendMessage
from nonebot.typing import T_State
from nonebot.params import State
from .config import Config

from ..utils.data import read_favor
from ..utils.message import build_forward_pic_message

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
Style = ['水彩', '油画', '粉笔画', '卡通', '蜡笔画', '儿童画']

draw_pic = on_command('作图')


@draw_pic.handle()
async def draw_pic_handle(bot: Bot, event: MessageEvent, state: T_State = State()):
    if read_favor(event.sender.id) < 3000:
        await draw_pic.finish("『×条件未满足』此功能要求好感度≥3000")
    if Working:
        await draw_pic.finish("『×当前有任务正在进行中』请稍后再试")
    des = event.get_plaintext()[4:].strip()
    if not des:
        await draw_pic.finish("『×参数错误』请输入正确的描述性文字\n[形容词] [主语] ，[细节设定]， [修饰语或者艺术家]")
    state['des'] = des


@draw_pic.got('style', prompt='请选择绘画风格，仅输入编号\n1.水彩\n2.油画\n3.粉笔画\n4.卡通\n5.蜡笔画\n6.儿童画')
async def draw_pic_got(bot: Bot, event: MessageEvent, state: T_State = State()):
    global Working
    index = str(state['style'])
    if not str(state['style']).isdigit():
        await draw_pic.finish('『×参数错误』请输入正确的绘画风格编号')
    index = int(index)
    if index > len(Style) or index < 1:
        await draw_pic.reject('『×参数错误』编号超出范围，请重新输入')
    style = Style[index-1]
    # 开始作图
    await draw_pic.send('开始作图，请稍后...这可能需要一段时间...')
    Working = True
    rst = TextToImage.create(text=state['des'], style=str(style))
    nodelist = await build_forward_pic_message(bot, rst['imgUrls'])
    Working = False
    if isinstance(event, GroupMessage):
        await bot.send_group_message(target=event.sender.group.id, message_chain=[{"type": "Forward", "nodeList": nodelist}])
    elif isinstance(event, FriendMessage):
        await bot.send_friend_message(target=event.sender.id, message_chain=[{"type": "Forward", "nodeList": nodelist}])
