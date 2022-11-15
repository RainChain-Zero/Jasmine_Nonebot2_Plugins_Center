import asyncio
import json
import aiohttp

with open(r'src\plugins\test\100question.json', encoding='utf-8') as f:
    text = f.read()
    j = json.loads(text)


async def post_question():
    async with aiohttp.ClientSession() as session:
        for i in j:
            async with session.post('http://localhost:45445/truth/addTruth', json={'questioner': '初始化', 'question': i}) as response:
                res = response.json()
                print(res)

asyncio.run(post_question())
