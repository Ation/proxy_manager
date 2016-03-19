import asyncio
import aiohttp
import time

import asyncproxymanager
import hidemyass
import fpl

class PendingCollection():
    def __init__(self):
        self._q = asyncio.Queue()
        self.pending_update = False

    async def update_items(self):
        print('Updating items in 2 sec')
        await asyncio.sleep(2)
        print('Putting items')
        await self._q.put(10)
        await self._q.put(20)
        await self._q.put(30)
        print('Items added')
        self.pending_update = False

    async def get_item(self):
        if self._q.empty():
            print('Q isempty')
            if not self.pending_update:
                print("Schedule update")
                self.pending_update = True
                asyncio.get_event_loop().create_task(self.update_items())
                print("Update scheduled")

        item = await self._q.get()
        return item


async def get_items(collection, task_id):
    for i in range(10):
        print(str(task_id) + ": getting item" )
        item = await collection.get_item()
        print(str(task_id) + ": get item " + str(item) )

    print("Task completed " + str(task_id))


def read_items(count):
    c = PendingCollection()
    tasks = []
    for i in range(count):
        tasks.append(get_items(c, i))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

async def secondary_task():
    print('Start secondary task')
    await asyncio.sleep(10)
    print('Out of secondary task')

async def main_task():
    print('Starting main task')
    await asyncio.sleep(1)
    print('Creating secondary task')
    asyncio.get_event_loop().create_task(secondary_task())
    await asyncio.sleep(1)
    print('Main task stopping loop')
    asyncio.get_event_loop().stop()


def test_stop():
    loop = asyncio.get_event_loop()
    print('Create main task')
    loop.create_task(main_task())
    print('Run forever')
    loop.run_forever()
    print('About to close loop')
    loop.close()
    print('Loop closed')

async def req_func():
    with aiohttp.Timeout(10):
        async with aiohttp.get("http://ya.ru") as response:
            if response.status == 200:
                print( await response.text() )

def test_http():

    asyncio.get_event_loop().run_until_complete(req_func())

def test_proxy():
    loop = asyncio.get_event_loop()
    pm = asyncproxymanager.AsyncProxyManager('https', auto_update = False, event_loop = loop)

    pm.add_provider(hidemyass.ProxyProvider())
    pm.add_provider(fpl.FPLProxyProvider())
    pm.add_provider(fpl.SSLProxyProvider())
    pm.add_provider(fpl.USProxyProvider())
    pm.add_provider(fpl.UKProxyProvider())

    loop.run_until_complete(pm.update_proxy_list())
    loop.close()

def main():
    # read_items(3)
    # test_stop()
    # test_http()
    test_proxy()

if __name__ == '__main__':
    main()