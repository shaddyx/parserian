import threading
import typing

from parserian.proxy import Proxy


class ProxyFactory:
    def __init__(self):
        self.proxies: typing.List[Proxy] = []
        self.index = 0
        self.local = threading.local()
        self.lock = threading.RLock()

    def load_from_file(self, filename):
        with open(filename, "r") as f:
            for line in f:
                self.add(Proxy(line.strip()))

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            for proxy in self.proxies:
                f.write("{}\n".format(proxy.url))

    def add(self, proxy):
        with self.lock:
            self.proxies.append(proxy)
            proxy.attach(self)

    def next(self):
        with self.lock:
            if self.index >= len(self.proxies):
                self.index = 0
            proxy = self.proxies[self.index]
            self.index += 1
            return proxy

    def start(self, proxy):
        self.local.proxy = proxy
        return proxy

    def proxy_error(self, exc_type, exc_val, exc_tb):
        with self.lock:
            if exc_type is None:
                self.local.proxy.success_count += 1
            else:
                self.local.proxy.failed_count += 1
                if self.local.proxy.should_be_deleted():
                    self.proxies.remove(self.local.proxy)
