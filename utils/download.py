import uuid
import aiohttp
import aiofiles


async def download_pic(url: str, path: str, proxy: str = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxy) as response:
            # 使用uuid1生成唯一图片名
            uid = str(uuid.uuid1()) + '.gif'
            fileName = path + uid
            async with aiofiles.open(fileName, 'wb') as afp:
                await afp.write(await response.content.read())
                return uid
