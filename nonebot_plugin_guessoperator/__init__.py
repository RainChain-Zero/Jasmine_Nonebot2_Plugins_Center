
import time
import json
from nonebot import get_driver, logger, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, MessageEvent
from nonebot import require

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

from .config import Config

from nonebot import get_driver

driver = get_driver()

global_config = get_driver().config
config = Config.parse_obj(global_config)

# 配置浏览器
opt = Options()
opt.add_argument('--headless')
opt.add_argument('--disable-gpu')
opt.add_argument('--window-size=1366,768')
opt.add_argument("--no-sandbox")
# opt.add_experimental_option("excludeSwitches", ["enable-logging"])
opt.add_argument('ignore-certificate-errors')

# 保存实例
BroswerDic = {}
# 记录当前群剩余次数
GroupCnt = {}
# 记录群最后问答时间
GroupLastTime = {}

# 触发器
StartTrigger = on_command("猜干员 ")
AnswerTrigger = on_command("看答案")
StopTrigger = on_command("不猜了")
SearchTrigger = on_command("查干员")


@StartTrigger.handle()
async def StartGame(event: GroupMessageEvent):
    global BroswerDic, GroupCnt, GroupLastTime

    # 获取干员
    operator = event.get_plaintext()[5:]
    # 当前群不存在浏览器实例
    if not BroswerDic.__contains__(event.group_id):
        await StartTrigger.send("茉莉正在执行初始化...请耐心等待\n若短时间内不使用，请输入“/不猜了”关闭相关进程")
        # 创建Chrome对象并传入设置信息.
        browser = webdriver.ChromiumEdge(options=opt)
        browser.get("http://akg.saki.cc")
        browser.implicitly_wait(2)
        BroswerDic[event.group_id] = browser
        try:
            browser.find_element(By.CSS_SELECTOR, '.close-icon').click()
        except:
            await StartTrigger.finish("网络连接出错！")

    BrowserNow = BroswerDic[event.group_id]
    # 当前群不存在次数配置
    if not GroupCnt.__contains__(event.group_id):
        GroupCnt[event.group_id] = 8

    # 更新群最后问答时间
    GroupLastTime[event.group_id] = time.time()
    try:
        input = BrowserNow.find_element(By.ID, 'guess')
        input.send_keys(operator)
    except:
        await StartTrigger.finish("当前进程网络连接失败！")
    # 判断干员名是否输入正确
    # ! 暂时弃用
    # try:
    #     time.sleep(0.5)
    #     # !自动补全（有待商榷）
    #     suggest = BrowserNow.find_element(
    #         By.CSS_SELECTOR, "#guessautocomplete-list div:first-child input").get_dom_attribute('value')
    #     # 排除可能补全bug
    #     if(operator != "红" and operator != "梅" and operator != "山" and operator != "黑" and operator != "w" and operator != "W"
    #        and operator != "阿"):
    #         input.clear()
    #         input.send_keys(suggest)
    # except:
    #     input.clear()
    #     await StartTrigger.finish("当前干员名称输入有误哦~")

    # todo 暂时采用本地信息
    # ! 注意文件路径
    data = json.load(open(
        r'/home/nonebot2/src/plugins/nonebot_plugin_guessoperator/operator.json', encoding='UTF-8'))
    if(not data.__contains__(operator)):
        input.clear()
        await StartTrigger.finish("当前干员名称输入有误哦~")

    # 剩余次数减一
    cnt = GroupCnt[event.group_id] = GroupCnt[event.group_id]-1

    BrowserNow.find_element(By.CSS_SELECTOR, '.mdui-btn-raised').click()

    # 截图结果 Base64编码
    pic = BrowserNow.find_element(
        By.CSS_SELECTOR, '.guesses').screenshot_as_base64

    # 尝试获取结果
    res = ""
    try:
        tmp = BrowserNow.find_element(
            By.CSS_SELECTOR, '.answer').get_attribute('innerText')
        res = tmp
    except:
        pass

    if(res.startswith("成功")):
        # 准备重新开始
        GroupCnt[event.group_id] = 8
        BrowserNow.find_element(
            By.CSS_SELECTOR, '.main-container .togglec').click()
    elif(cnt <= 0):
        # 显示答案
        res = BrowserNow.find_element(
            By.CSS_SELECTOR, '.answer').get_attribute('innerText')
        # 准备重新开始
        GroupCnt[event.group_id] = 8
        BrowserNow.find_element(
            By.CSS_SELECTOR, '.main-container .togglec').click()

    msg = f"『干员猜猜乐』当前剩余次数{cnt}/8\n"+MessageSegment.image(None, None, None, pic)
    if(res != ""):
        msg += f"\n{res}\n\n当前可直接输入“/猜干员 [干员名]继续”"

    input.clear()
    await StartTrigger.finish(msg)


@AnswerTrigger.handle()
async def GiveAnswer(event: GroupMessageEvent):
    global GroupCnt, BroswerDic
    try:
        browser = BroswerDic[event.group_id]
        browser.find_element(By.CSS_SELECTOR, '.togglec').click()
        browser.find_element(
            By.CSS_SELECTOR, '.mdui-dialog-actions a:nth-child(2)').click()
        res = browser.find_element(
            By.CSS_SELECTOR, '.answer').get_attribute('innerText')
    except:
        logger.warning("guessoperator:获取答案失败！")

    # 准备重新开始
    GroupCnt[event.group_id] = 8

    try:
        browser.find_element(
            By.CSS_SELECTOR, '.main-container .togglec').click()
    except:
        logger.warning("guessoperator:获取答案后开启新的一轮失败")

    await AnswerTrigger.finish(res+"\n\n当前可直接输入“/猜干员 [干员名]继续")


@StopTrigger.handle()
async def StopGame(event: GroupMessageEvent):
    global GroupCnt, BroswerDic
    if(GroupCnt.__contains__(event.group_id) and BroswerDic.__contains__(event.group_id)):
        del GroupCnt[event.group_id]
        # 关闭浏览器实例
        try:
            BroswerDic[event.group_id].refresh()
            BroswerDic[event.group_id].delete_all_cookies()
            BroswerDic[event.group_id].quit()
            del BroswerDic[event.group_id]
        except:
            pass
    await StopTrigger.finish("茉莉已成功关闭本轮猜题")

# 定时检查关闭浏览器实例
scheduler = require("nonebot_plugin_apscheduler").scheduler


async def ClearBroswer():
    # 遍历时要修改dic，将key转为列表
    for group in list(BroswerDic.keys()):
        if(GroupLastTime.__contains__(group)):
            # 超过20分钟未进行问答
            if(time.time()-GroupLastTime[group] > 1200):
                logger.warning("guessoperator:已执行一轮清除")
                del GroupCnt[group]
                try:
                    BroswerDic[group].refresh()
                    BroswerDic[group].delete_all_cookies()
                    BroswerDic[group].quit()
                    del BroswerDic[group]
                except:
                    pass

scheduler.add_job(ClearBroswer, "interval", minutes=25, id="guessoperator")


# 退出时关闭所有实例
@driver.on_shutdown
async def do_something():
    for group in list(BroswerDic.keys()):
        try:
            BroswerDic[group].refresh()
            BroswerDic[group].delete_all_cookies()
            BroswerDic[group].quit()
            del BroswerDic[group]
        except:
            pass


@SearchTrigger.handle()
async def SearchOperator(event: MessageEvent):
    operator = event.get_plaintext()[5:]
    #! 注意文件路径
    data = json.load(open(
        r'/home/nonebot2/src/plugins/nonebot_plugin_guessoperator/operator.json', encoding='UTF-8'))
    if(data.__contains__(operator)):
        await SearchTrigger.finish(data[operator])
    else:
        await SearchTrigger.finish("当前干员名称输入有误哦~")
