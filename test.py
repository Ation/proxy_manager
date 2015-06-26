import proxymanager
import hidemyass

def main():
    proxy_manager = proxymanager.ProxyManager()
    hma_provider = hidemyass.ProxyProvider()

    proxy_manager.add_proxy_provider(hma_provider)

    proxy_manager.update_proxy_list('HTTPS')

    while True:
        proxy = proxy_manager.get_proxy()
        if proxy is None:
            break

        print(proxy.get_ip() + ':' + proxy.get_port() + ' ( ' + proxy.get_type() + ' )' )

if __name__ == '__main__':
    main()