from email import header
from multiprocessing.connection import Client
import aiohttp
from nonebot import Bot, get_driver, on_command, on_regex

from .config import Config

from nonebot.adapters.mirai2 import MessageEvent, MessageSegment, MessageChain

global_config = get_driver().config
config = Config.parse_obj(global_config)


async def httpPost(origin):
    # api地址
    url = "https://lab.magiconch.com/api/nbnhhsh/guess"
    # 书写头部
    headers = {
        'origin': 'https://lab.magiconch.com',
        'referer': 'https://lab.magiconch.com/nbnhhsh/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
    }
    # data
    data = {
        'text': f'{origin}'
    }
    # aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as response:
            res = await response.json()
            if res:
                return res
            else:
                return []


async def addnew(item, new):
    url = 'https://lab.magiconch.com/api/nbnhhsh/translation/'+item
    headers = {
        'origin': 'https://lab.magiconch.com',
        'referer': 'https://lab.magiconch.com/nbnhhsh/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
    }
    data = {
        'text': f'{new}'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as response:
            pass

# matcher
sx_matcher = on_command("sx", None, {"缩写"})


@sx_matcher.handle()
async def sxHandler(bot: Bot, event: MessageEvent):
    # 截取
    origin = str(event.get_message())[3:]
    # 中文拦截
    for ch in origin:
        if u'\u4e00' <= ch <= u'\u9fff':
            await sx_matcher.finish("名词只能是缩写哦，不支持中文")
    res = await httpPost(origin)
    msg = ""
    try:
        res = res[0]
        name = res['name']  # 这里主要是为了输出时避免可能的前置空格
        try:
            trans = res['trans']
            msg += ','.join(trans)
        except KeyError:
            pass
        try:
            inputs = res['inputting']
            msg += ','.join(inputs)
        except KeyError:
            pass
        if msg:
            # msgChain=MessageChain([,])
            # 注意获取消息id的方法MessageEvent.source.id
            await sx_matcher.finish(MessageSegment.plain(f'{name}的解释为:\n{msg}'))
        else:
            await sx_matcher.finish(f'茉莉没有找到{origin}的解释呢...')
    except KeyError:
        await sx_matcher.finish('唔...茉莉发现有哪里出错了呢')

sx_add = on_command("sx add")


@sx_add.handle()
async def sxaddHandle(event: MessageEvent):
    tmp = str(event.get_message())[8:]
    tmplist = tmp.split(" ")
    if len(tmplist) <= 1:
        await sx_add.finish("参数有误啦！")
    item = tmplist[0]
    for ch in item:
        if u'\u4e00' <= ch <= u'\u9fff':
            await sx_add.finish("名词只能是缩写哦，不支持中文")
    new = tmplist[1]
    await addnew(item, new)
    await sx_add.finish(f"茉莉已经提交{item}的补充解释")
