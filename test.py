import proxymanager
import hidemyass
import fpl

import requests

def test_proxy(proxy):
    attempts = 0

    http_result = test_http(proxy)
    https_result = test_https(proxy)

    return http_result, https_result

def test_http(proxy):
    attempts = 0
    while attempts < 3:
        s = requests.Session()
        url = 'http://ya.ru'
        s.proxies = { 'http': 'http://'+proxy.get_ip()+':'+proxy.get_port() }

        try:
            r = s.get(url, timeout = 1)
            if r.status_code == 200:
                return True
        except:
            pass

        attempts += 1

    return False

def test_https(proxy):
    attempts = 0
    while attempts < 3:
        s = requests.Session()
        url = 'https://ya.ru'
        s.proxies = { 'https': 'https://'+proxy.get_ip()+':'+proxy.get_port() }

        try:
            r = s.get(url, timeout = 1)
            if r.status_code == 200:
                return True
        except:
            pass

        attempts += 1

    return False

def test_provider(provider):
    working = 0
    failed = 0

    proxy_manager = proxymanager.ProxyManager()

    proxy_manager.add_proxy_provider(provider)
    proxy_manager.update_proxy_list()

    while True:
        proxy = proxy_manager.get_proxy()
        if proxy is None:
            break

        print('Testing: ' + proxy.get_ip() + ':' + proxy.get_port() + ' ( ' + proxy.get_type() + ' )' )
        http_result, https_result = test_proxy(proxy)
        print ('  HTTP: ' + ' OK' if http_result else 'FAILED')
        print ('  HTTPS: ' + ' OK' if https_result else 'FAILED')

        if http_result or https_result:
            working += 1
        else:
            failed += 1

    return working, failed

class ProviderTest:
    def __init__(self, name, provider):
        self._name = name
        self._provider = provider

    def run_test(self):
        print('Running tests for : ' + self._name)
        print('')

        self._working = 0
        self._failed = 0

        proxy_manager = proxymanager.ProxyManager()

        proxy_manager.add_proxy_provider(self._provider)
        proxy_manager.update_proxy_list()

        while True:
            proxy = proxy_manager.get_proxy()
            if proxy is None:
                break

            print('Testing: ' + proxy.get_ip() + ':' + proxy.get_port() + ' ( ' + proxy.get_type() + ' )' )
            http_result, https_result = test_proxy(proxy)
            print ('  HTTP: ' + ' OK' if http_result else 'FAILED')
            print ('  HTTPS: ' + ' OK' if https_result else 'FAILED')

            if http_result or https_result:
                self._working += 1
            else:
                self._failed += 1

    def __str__(self):
        return ''.join( [self._name, ' test results\n', '  Working : ', str(self._working), '\n  Failed  : ', str(self._failed) ] )


def main():
    tests =  [  ProviderTest('HideMyAss', hidemyass.ProxyProvider()),
                ProviderTest('FPL', fpl.FPLProxyProvider()),
                ProviderTest('SSL', fpl.SSLProxyProvider()),
                ProviderTest('US', fpl.USProxyProvider()),
                ProviderTest('UK', fpl.UKProxyProvider()) ]

    for t in tests:
        t.run_test()

    for t in tests:
        print(t)

if __name__ == '__main__':
    main()