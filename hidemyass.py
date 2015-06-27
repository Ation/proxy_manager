import json
import re
import requests
import socket

import proxy

import xml.etree.ElementTree as ET

def is_number(number):
    try:
        int(number)
        return True
    except:
        return False


class HMA_Proxy(proxy.Proxy):
    def __init__(self, ip, port, proxy_type='HTTP', speed='100', connection_time='100'):
        proxy.Proxy.__init__(self, ip, port, proxy_type)

        self._speed = speed
        self._connection_time = connection_time

    def get_speed(self):
        return self._speed

    def get_connectiontime(self):
        return self._connection_time

class ProxyProvider:
    def __init__(self):
        self.headers = {
            'User-Agent':'grabber',
            'Accept':'application/json',
            # 'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive',
            'X-Requested-With':'XMLHttpRequest'
            }
        self._session = requests.Session()

    def get_proxy_list(self, proxy_type):
        pages_count = self._get_pages_count()

        proxy_list = []

        for index in range(1, pages_count+1):
            page_html = self._getpage(index)
            entries = self._extract_entries(page_html)

            for entry in entries:
                proxy = self._extract_proxy(entry)
                if proxy_type == None or proxy.get_type() == proxy_type:
                    proxy_list.append( self._extract_proxy(entry) )

        return proxy_list

    def _getpage(self, index):
        page = self._session.get("http://proxylist.hidemyass.com/"+str(index), headers=self.headers)

        if page.status_code != 200:
            print( "Code: " + str(page.status_code) )
            return None

        return page.text

    def _get_pages_count(self):
        html = self._getpage(1)
        if not html:
            return -1

        data = json.loads(html)

        pages = re.findall( r'<a href="/\d+?">(\d+?)</a>', data['pagination'])

        pages = [int(c) for c in pages]
        pages = sorted(pages)

        return pages[-1]

    def _extract_entries(self, html):
        data = json.loads(html)

        valid_xml = ''.join(['<data>',data['table'].replace('<td nowrap>', '<td>'),'</data>'])
        root = ET.fromstring(valid_xml)

        return root

    def _extract_proxy(self, xml_element):
        ip = self._extract_ip(xml_element)

        port = xml_element[2].text
        connection_type = xml_element[6].text

        speed = self._extract_width(xml_element[4])
        connection_time = self._extract_width(xml_element[5])

        return HMA_Proxy(ip, port, connection_type, speed, connection_time)

    def _extract_ip(self, xml_element):
        ip_element = xml_element[1][0]
        ip = ''

        required = '{display:inline}'
        stylestring = ip_element.find('style').text

        styles = [ style.replace(required, '')[1:] for style in stylestring.splitlines() if required in style]

        for el in ip_element:
            if el.tag == 'span':
                el_class = el.get('class')
                if el_class and (el_class in styles or is_number(el_class)):
                    ip+=el.text
                else:
                    style = el.get('style')
                    if style and 'inline' in style:
                        ip+=el.text
            if el.tail and len(el.tail) != 0:
                ip+=el.tail

        return ip

    def _extract_width(self, xml_element):
        style = xml_element[0][0].get('style')

        return re.findall(r'width: (\d+?)%', style)[0]