import proxy
import re
import xml.etree.ElementTree as ET

import requests

class FPLProxyProvider:
    def __init__(self):
        self._session = requests.Session()

    def get_proxy_list(self, proxy_type = None):
        return self._get_proxy_list_form_url('http://free-proxy-list.net/', proxy_type)

    def _get_proxy_list_form_url(self, url, proxy_type_filter = None):
        response = self._session.get(url)
        if response.status_code != 200:
            raise Exception('Failed to load page')

        data = re.findall(r'<tbody>.*</tbody>', response.text, flags = re.DOTALL)
        root = ET.fromstring(data[0])

        result = []

        for entry in root:
            ip = entry[0].text
            port = entry[1].text
            proxy_type = 'HTTPS' if entry[6].text == 'yes' else 'HTTP'

            if proxy_type_filter is None or proxy_type_filter == proxy_type:
                result.append( proxy.Proxy(ip, port, proxy_type) )

        return result


class SSLProxyProvider(FPLProxyProvider):
    def get_proxy_list(self, proxy_type = None):
        return self._get_proxy_list_form_url('http://sslproxies.org/', proxy_type)


class USProxyProvider(FPLProxyProvider):
    def get_proxy_list(self, proxy_type = None):
        return self._get_proxy_list_form_url('http://us-proxy.org/', proxy_type)


class UKProxyProvider(FPLProxyProvider):
    def get_proxy_list(self, proxy_type = None):
        return self._get_proxy_list_form_url('http://free-proxy-list.net/uk-proxy.html', proxy_type)