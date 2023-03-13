from typing import List
import aiohttp
from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)


async def get_truth(qq: str) -> object:
    async with aiohttp.ClientSession() as session:
        async with session.get(config.url+'getTruth', params={'qq': qq}) as response:
            resp = await response.json()
            return resp['data']


async def add_truth(questioner: str, question: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(config.url+'addTruth', json={'questioner': questioner, "question": question}) as response:
            resp = await response.json()
            return resp['succ']


async def answer_truth(qq: str, id: int, answer: str) -> bool:
    async with aiohttp.ClientSession() as session:
        print(answer)
        async with session.post(config.url+'answerTruth', json={'qq': qq, "id": id, "answer": answer}) as response:
            resp = await response.json()
            return resp['succ']


async def get_truth_history(qq: str, id: int) -> List:
    async with aiohttp.ClientSession() as session:
        async with session.get(config.url+'getTruthHistory', params={'qq': qq, 'id': id}) as response:
            resp = await response.json()
            if resp['succ']:
                return resp['data']
            return '获取回答失败，请联系管理员'


async def clear_truth_answered(qq: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.delete(config.url+'clearTruthAnswered', params={'qq': qq}) as response:
            resp = await response.json()
            return resp['succ']


async def get_history_list(qq: str) -> List:
    async with aiohttp.ClientSession() as session:
        async with session.get(config.url+'getHistoryList', params={'qq': qq}) as response:
            resp = await response.json()
            if resp['succ']:
                return resp['data']
            return None
