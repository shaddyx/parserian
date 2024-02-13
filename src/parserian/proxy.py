import threading


class Proxy:
    def __init__(self, url):
        self.url = url
        self.failed_count = 0
        self.success_count = 0
        self.last_used_time = 0
        self.acquired = False
        self.last_error_time = 0
        self.lock = threading.RLock()
        self.factory = None

    def attach(self, factory):
        if self.factory is not None:
            raise Exception("proxy already attached")
        self.factory = factory

    def success(self):
        with self.lock:
            self.success_count += 1

    def fail(self):
        with self.lock:
            self.failed_count += 1

    def should_be_deleted(self):
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.factory._proxy_error(self, exc_type, exc_val, exc_tb)

    def __str__(self):
        return "{}[{}]".format(self.__class__.__name__, self.url)


class HttpProxy(Proxy):
    pass


class Socks5Proxy(Proxy):
    pass
