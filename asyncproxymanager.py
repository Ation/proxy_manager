import asyncio
import aiohttp
import time

import sys

class AsyncProxyManager:
    def __init__(self, proxy_type, auto_update = True, event_loop = None):
        self._proxy_type = proxy_type.lower()

        if self._proxy_type != 'https' and self._proxy_type != 'http':
            raise ValueError('invalid proxy type')

        self._testing_url = self._proxy_type + '://ya.ru'

        self._proxy_providers = []
        self._proxy_list = asyncio.Queue()
        self._update_in_process = False
        self._auto_update = auto_update
        if event_loop is None:
            self._event_loop = asyncio.get_event_loop()
        else:
            self._event_loop = event_loop

    def add_provider(self, provider):
        self._proxy_providers.append(provider)

    def schedule_update(self):
        if self._proxy_list.empty():
            if not self._update_in_process:
                self._update_in_process = True
                self._event_loop.create_task(self.update_proxy_list())
        return

    async def get_verified_proxy(self):
        if self._proxy_list.empty():
            if not self._auto_update:
                return None

        self.schedule_update()
        proxy = await self._proxy_list.get()
        self.schedule_update()

        return proxy

    async def check_proxy(self, proxy):
        attempts = 0
        max_attempts = 3
        max_timeout = 10
        while attempts < max_attempts:
            proxy_string = 'http://' + proxy.get_ip() + ':' + proxy.get_port()
            print('Testing proxy: ' + proxy_string)

            with aiohttp.Timeout( max_timeout ):
                connector = aiohttp.ProxyConnector(
                    proxy = proxy_string)
                with aiohttp.ClientSession(connector=connector) as session:
                    try:
                        async with session.get(self._testing_url) as response:
                            if response.status == 200:
                                await self._proxy_list.put( proxy )
                                print('Adding proxy: ' + proxy_string)
                                return True
                    except TypeError as te:
                        print('Type error : ', te)
                        pass
                    except:
                        print('Exception on GET request: ', sys.exc_info()[0])
                        pass

            attempts += 1
        print('Proxy is down : ' + proxy_string)
        return False

    async def update_proxy_list(self):
        new_proxy_list = []

        print('Start updating proxy list')

        for pp in self._proxy_providers:
            new_proxy_list.extend(pp.get_proxy_list(None))

        print('Start checking proxy list : ' + str(len(new_proxy_list)))
        print('Testing url               : ' + self._testing_url)

        # check new proxy list and add valid proxy
        pending = set()
        max_pending = 10
        # max interval in seconds
        max_wait_time = 0.1
        for index, proxy_to_test in enumerate(new_proxy_list):
            pending.add( asyncio.ensure_future( self.check_proxy(proxy_to_test), loop = self._event_loop))

            print('Pending tasks: ' + str(len(pending)))

            if index != ( len(new_proxy_list) - 1) and len(pending) < max_pending:
                continue

            start_time = time.time()
            done, pending = await asyncio.wait(pending, loop = self._event_loop, return_when = asyncio.FIRST_COMPLETED)
            end_time = time.time()

            wait_time = end_time - start_time
            print('Wait time : ' + str(wait_time))
            if wait_time > max_wait_time:
                max_pending = max_pending + 1
                print('Increasing max_pending to: ' + str(max_pending))

        if len(pending) != 0:
            print('Waiting for rest pending proxy to test')
            done, pending = await asyncio.wait(pending, loop = self._event_loop, return_when = asyncio.ALL_COMPLETED)

        print('Proxy list update completed. Added: ' + str(self._proxy_list.qsize()))
