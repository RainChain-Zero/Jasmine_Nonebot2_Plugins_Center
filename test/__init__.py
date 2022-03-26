'''
Author: your name
Date: 2022-03-22 21:54:37
LastEditTime: 2022-03-26 18:31:43
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \nonebot\src\plugins\test\__init__.py
'''
import base64
from nonebot import get_driver, on_command
from nonebot.adapters.mirai2 import MessageEvent,GroupMessage,MessageChain,MessageSegment
from PIL import Image
from .config import Config
from playwright.async_api import async_playwright,Browser
from io import BytesIO

global_config = get_driver().config
config = Config.parse_obj(global_config)

driver=get_driver()


test=on_command("测试")

@test.handle()
async def _ (event:MessageEvent):
    async with async_playwright()as p:
        browser=await p.webkit.launch()
        context=await browser.new_context()
        page=await context.new_page()
        await page.goto("https://www.baidu.com/")

        await test.finish(MessageSegment.image(None,None,None,base64.b64encode(BytesIO(await page.screenshot()).getvalue())))

# @driver.on_startup
# async def pluginstart():
#     global browser
#     async with async_playwright()as p:
#         browser=await p.webkit.launch()


