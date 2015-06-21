

class Proxy:
    def __init__(self, ip, port, proxy_type):
        self._ip = ip
        self._port = port
        self._type = proxy_type

    def get_ip(self):
        return self._ip

    def get_port(self):
        return self._port

    def get_type(self):
        return self._type