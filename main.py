from typing import Optional

import aiohttp
import asyncio


def url(port: int, scenario: int, param: Optional[str] = None):
    base_url = f'http://localhost:{port}/{scenario}'
    if param:
        return base_url + f'?{param}'
    return base_url


class FirstCompletedTaskGroup(asyncio.TaskGroup):
    def __init__(self):
        super().__init__()
        self.__tasks = []
        self.winner = None

    def cancel_others(self, task):
        if not task.cancelled():
            self.__tasks.remove(task)
            for t in self.__tasks:
                t.cancel()
            self.winner = task.result()

    def create_task(self, coro, *, name=None, context=None):
        task = super().create_task(coro, name=name, context=context)
        task.add_done_callback(self.cancel_others)
        self.__tasks.append(task)
        return task

    def result(self):
        return self.winner


# note: requires increasing max number of open files `ulimit -n 16000`
async def scenario3(port: int):
    connector = aiohttp.TCPConnector(limit=10_000)
    async with aiohttp.ClientSession(connector=connector) as session:
        async def req():
            async with session.get(url(port, 3)) as response:
                return await response.text()

        async with FirstCompletedTaskGroup() as group:
            [group.create_task(req()) for _ in range(10_000)]

        return group.result()


async def main():
    result3 = await scenario3(8080)
    print(result3)

if __name__ == "__main__":
    asyncio.run(main())
