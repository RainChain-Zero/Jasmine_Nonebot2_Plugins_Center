from nonebot import get_driver, on_command
from nonebot.adapters.mirai2 import Bot, MessageEvent
from nonebot.typing import T_State
from nonebot.params import State
from .config import Config

from ..utils.data import read_favor

# 引入作图api工具包
from wenxin_api.tasks.text_to_image import TextToImage

global_config = get_driver().config
config = Config.parse_obj(global_config)

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
    await draw_pic.send('请选择绘画风格，仅输入编号\n1.水彩\n2.油画\n3.粉笔画\n4.卡通\n5.蜡笔画\n6.儿童画')


@draw_pic.got('style', prompt='请输入绘画风格')
async def draw_pic_got(bot: Bot, event: MessageEvent, state: T_State = State()):
    if not str(state['style'].isdigit()):
        await draw_pic.finish('『×参数错误』请输入正确的绘画风格编号')
    if int(state['style']) > len(Style) or int(state['style']) < 1:
        await draw_pic.finish('『×参数错误』请输入正确的绘画风格编号')
    style = Style[int(state['style'])-1]
