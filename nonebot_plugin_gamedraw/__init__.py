import asyncio
from operator import imod
import traceback
from cn2an import cn2an
from dataclasses import dataclass
from typing import Optional, Set, Tuple, Union

import nonebot
from nonebot import on_command, on_regex, on_keyword
from nonebot.adapters.mirai2 import MessageEvent
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import RegexGroup
from nonebot.permission import SUPERUSER
from nonebot.typing import T_Handler
from nonebot_plugin_apscheduler import scheduler

from .handles.base_handle import BaseHandle
from .handles.azur_handle import AzurHandle
from .handles.fgo_handle import FgoHandle
from .handles.genshin_handle import GenshinHandle
from .handles.guardian_handle import GuardianHandle
from .handles.onmyoji_handle import OnmyojiHandle
from .handles.pcr_handle import PcrHandle
from .handles.pretty_handle import PrettyHandle
from .handles.prts_handle import PrtsHandle

from .config import draw_config

from nonebot.adapters.mirai2 import MessageSegment
@dataclass
class Game:
    keywords: Set[str]
    handle: BaseHandle
    flag: bool
    max_count: int = 180  # 一次最大抽卡数
    reload_time: Optional[int] = None  # 重载UP池时间（小时）


games = (
    Game({"/azur", "/碧蓝", "/碧蓝航线"}, AzurHandle(), draw_config.AZUR_FLAG),
    Game({"/fgo", "/命运冠位指定"}, FgoHandle(), draw_config.FGO_FLAG),
    Game(
        {"/genshin", "/原神"},
        GenshinHandle(),
        draw_config.GENSHIN_FLAG,
        max_count=180,
        reload_time=18,
    ),
    Game(
        {"/guardian", "/坎公骑冠剑"},
        GuardianHandle(),
        draw_config.GUARDIAN_FLAG,
        reload_time=4,
    ),
    Game({"/onmyoji", "/阴阳师"}, OnmyojiHandle(), draw_config.ONMYOJI_FLAG),
    Game({"/pcr", "/公主连结", "/公主连接", "/公主链接", "/公主焊接"}, PcrHandle(), draw_config.PCR_FLAG),
    Game(
        {"/pretty", "/马娘", "/赛马娘"},
        PrettyHandle(),
        draw_config.PRETTY_FLAG,
        max_count=200,
        reload_time=4,
    ),
    Game({"/prts", "/方舟", "/明日方舟"}, PrtsHandle(), draw_config.PRTS_FLAG, reload_time=4),
)


def create_matchers():
    def draw_handler(game: Game) -> T_Handler:
        async def handler(
            matcher: Matcher, event: MessageEvent, args: Tuple[str, ...] = RegexGroup()
        ):
            pool_name, num, unit = args
            if num == "单":
                num = 1
            else:
                try:
                    num = int(cn2an(num, mode="smart"))
                except ValueError:
                    await matcher.finish("诶？茉莉看不懂你想抽什么呢..")
            if unit == "井":
                num *= game.max_count
            if num < 1:
                await matcher.finish("噫呼，这让茉莉怎么抽嘛")
            elif num > game.max_count:
                await matcher.finish("太贪心可不好哦？")
            pool_name = (
                pool_name.replace("池", "")
                .replace("武器", "arms")
                .replace("角色", "char")
                .replace("卡牌", "card")
                .replace("卡", "card")
            )
            try:
                res = game.handle.draw(num, pool_name=pool_name, user_id=event.get_user_id())
            except:
                logger.warning(traceback.format_exc())
                await matcher.finish("茉莉发现有哪里出错了...")
            await matcher.finish(res, at_sender=True)

        return handler

    def update_handler(game: Game) -> T_Handler:
        async def handler(matcher: Matcher):
            await game.handle.update_info()
            await matcher.finish("茉莉更新目标完成了！")

        return handler

    def reload_handler(game: Game) -> T_Handler:
        async def handler(matcher: Matcher):
            res = await game.handle.reload_pool()
            if res:
                await matcher.finish(res)

        return handler

    def reset_handler(game: Game) -> T_Handler:
        async def handler(matcher: Matcher, event: MessageEvent):
            if game.handle.reset_count(event.get_user_id()):
                await matcher.finish("茉莉重置目标成功了！")

        return handler

    def scheduled_job(game: Game) -> T_Handler:
        async def handler():
            await game.handle.reload_pool()

        return handler

    for game in games:
        pool_pattern = r"([^\s单0-9零一二三四五六七八九百十]{0,3})"
        num_pattern = r"(单|[0-9零一二三四五六七八九百十]{1,3})"
        unit_pattern = r"([抽|井|连])"
        draw_regex = r".*?(?:{})\s*{}\s*{}\s*{}".format(
            "|".join(game.keywords), pool_pattern, num_pattern, unit_pattern
        )
        update_keywords = {f"更新{keyword}信息" for keyword in game.keywords}
        reload_keywords = {f"重载{keyword}卡池" for keyword in game.keywords}
        reset_keywords = {f"重置{keyword}抽卡" for keyword in game.keywords}
        if game.flag:
            on_regex(draw_regex, priority=5, block=True).append_handler(
                draw_handler(game)
            )
            on_keyword(
                update_keywords, permission=SUPERUSER, priority=1, block=True
            ).append_handler(update_handler(game))
            on_keyword(reload_keywords, priority=1, block=True).append_handler(
                reload_handler(game)
            )
            on_keyword(reset_keywords, priority=1, block=True).append_handler(
                reset_handler(game)
            )
            if game.reload_time:
                scheduler.add_job(
                    scheduled_job(game), trigger="cron", hour=game.reload_time, minute=1
                )


create_matchers()


# 更新资源
@scheduler.scheduled_job(
    "cron",
    hour=4,
    minute=1,
)
async def _():
    tasks = []
    for game in games:
        if game.flag:
            tasks.append(asyncio.ensure_future(game.handle.update_info()))
    await asyncio.gather(*tasks)


driver = nonebot.get_driver()


@driver.on_startup
async def _():
    tasks = []
    for game in games:
        if game.flag:
            game.handle.init_data()
            if not game.handle.data_exists():
                tasks.append(asyncio.ensure_future(game.handle.update_info()))
    await asyncio.gather(*tasks)

# 用户帮助文档
helphandle=on_command("help抽卡",None,{"help 抽卡"})

@helphandle.handle()
async def helpdraw():
    await helphandle.finish(MessageSegment.image(None,None,"/home/mirai/Dice3349795206/plugin/HelpPic/drawcard.png",None))