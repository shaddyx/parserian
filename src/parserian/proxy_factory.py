import threading
import time
import typing

from parserian.proxy import Proxy


class ProxyFactory:

    def __init__(self):
        import parserian.proxy_rotation_strategy as proxy_strategy
        self.proxies: typing.List[Proxy] = []
        self.index = 0
        self.lock = threading.RLock()
        self.strategy = proxy_strategy.RoundRobinProxyStrategy()

    def load_from_file(self, filename):
        """
        Loads a list of proxies from a file in the next format:

        protocol://host:port

        example: http://1.1.1.1:8080

        :param filename:
        :return:
        """
        with open(filename, "r") as f:
            for line in f:
                self.add(Proxy(line.strip()))

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            for proxy in self.proxies:
                f.write("{}\n".format(proxy.url))

    def add(self, proxy: Proxy):
        with self.lock:
            self.proxies.append(proxy)
            proxy.attach(self)

    def next(self):
        """
        Returns the next available proxy
        If proxy is not available the ProxyNotAvailableException will be raised
        :return:
        :raises proxy_strategy.ProxyNotAvailableException
        """
        with self.lock:
            proxy = self.strategy.next(self)
            proxy.last_used_time = time.time()
            return proxy

    def _proxy_error(self, proxy, exc_type, exc_val, exc_tb):
        with self.lock:
            proxy.last_used_time = time.time()
            proxy.acquired = False
            if exc_type is None:
                proxy.success_count += 1
            else:
                proxy.failed_count += 1
                if proxy.should_be_deleted():
                    self.proxies.remove(proxy)
