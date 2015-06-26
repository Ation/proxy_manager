import collections

class ProxyManager:
    def __init__(self):
        self._proxy_list = collections.deque()
        self._proxy_providers = []

    def get_proxy(self):
        if len(self._proxy_list) == 0:
            return None

        return self._proxy_list.pop()

    def add_proxy_provider(self, provider):
        self._proxy_providers.append(provider)

    def update_proxy_list(self, proxy_type = None):
        for provider in self._proxy_providers:
            self._proxy_list.extend( provider.get_proxy_list(proxy_type) )

