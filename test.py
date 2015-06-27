import proxymanager
import hidemyass

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

def main():
    proxy_manager = proxymanager.ProxyManager()
    hma_provider = hidemyass.ProxyProvider()

    proxy_manager.add_proxy_provider(hma_provider)

    proxy_manager.update_proxy_list()

    working = 0
    failed = 0

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

    print("Failed: " + str(failed))
    print('Working' + str(working))

if __name__ == '__main__':
    main()