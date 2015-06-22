
class Proxy:
    def __init__(self, ip, port=80, proxy_type='HTTP'):
        self._ip = ip
        self._port = port
        self._type = proxy_type

    def get_ip(self):
        return self._ip

    def get_port(self):
        return self._port

    def get_type(self):
        return self._type

    def __eq__(self, other):
        try:
            return self._ip == other.get_ip() and self._port == other.get_port() and self._type == other.get_type()
        except:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return (self._ip +  str(self._port) + self._type).__hash__()