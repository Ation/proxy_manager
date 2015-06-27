import proxymanager
import hidemyass

import requests

def test_proxy(proxy):
    attempts = 0
    while attempts < 3:
        s = requests.Session()
        if proxy.get_type() == 'HTTP':
            url = 'http://ya.ru'
            s.proxies = { 'http': 'http://'+proxy.get_ip()+':'+proxy.get_port() }
        elif proxy.get_type() == 'HTTPS':
            url = 'https://ya.ru'
            s.proxies = { 'https': 'https://'+proxy.get_ip()+':'+proxy.get_port() }
        else:
            url = 'http://ya.ru'

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

    proxy_manager.update_proxy_list('HTTPS')

    working = 0
    failed = 0

    while True:
        proxy = proxy_manager.get_proxy()
        if proxy is None:
            break

        print('Testing: ' + proxy.get_ip() + ':' + proxy.get_port() + ' ( ' + proxy.get_type() + ' )' )
        if test_proxy(proxy):
            print('working')
            working += 1
        else:
            print('failed')
            failed += 1


    print("Failed: " + str(failed))
    print('Working' + str(working))

if __name__ == '__main__':
    main()