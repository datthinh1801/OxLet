import asyncio
import json
from aiohttp import ClientSession

from utils import crawl_resource


async def create_new_note(session: ClientSession, word: str):
    result = await crawl_resource(session, word)
    data = json.dumps(result).encode('utf-8')
    # resp = await session.post(url='http://localhost:8765', data=json.dumps(data).encode('utf-8'))


async def check_model_exist(session: ClientSession) -> bool:
    model_name = 'English (by datthinh1801)'
    modelnames_request = {"action": "modelNames", "version": 6}
    resp = await session.post(url='http://localhost:8765', data=json.dumps(modelnames_request).encode('utf-8'))
    resp_json = json.loads(await resp.text())
    return resp_json['error'] is None and 'English (by datthinh1801)' in resp_json['result']


async def main(word):
    async with ClientSession(headers={"User-Agent": "Chrome"}) as session:
        # await create_new_note(session, word)
        print(await check_model_exist(session))


if __name__ == '__main__':
    asyncio.run(main('imperceptible'))
