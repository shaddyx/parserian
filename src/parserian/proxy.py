import threading


def _parse_url(url: str):
    try:
        if "://" not in url:
            url = "http://" + url
        protocol = url.split("://")[0]
        hostport = url.split("://")[1]
        username = None
        password = ""
        if "@" in hostport:
            username_pass = hostport.split("@")[0]
            hostport = hostport.split("@")[1]
            username = username_pass.split(":")[0]
            password = username_pass.split(":")[1]
        if ":" not in hostport:
            hostport = hostport + ":80"
        host = hostport.split(":")[0]
        port = int(hostport.split(":")[1])
        return protocol, host, port, username, password
    except Exception as e:
        raise Exception("Failed to parse url: {}".format(url)) from e


class Proxy:
    def __init__(self, url):
        parsed = _parse_url(url)
        self.protocol = parsed[0]
        self.host = parsed[1]
        self.port = parsed[2]
        self.username = parsed[3]
        self.password = parsed[4]
        self.failed_count = 0
        self.success_count = 0
        self.last_used_time = 0
        self.acquired = False
        self.last_error_time = 0
        self.lock = threading.RLock()
        self.factory = None

    @property
    def url(self):
        if self.username is None:
            return "{}://{}:{}".format(self.protocol, self.host, self.port)
        else:
            return "{}://{}:{}@{}:{}".format(self.protocol, self.username, self.password, self.host, self.port)

    def playwright_proxy(self):
        if self.username is None:
            return {
                "server": "{}://{}:{}".format(self.protocol, self.host, self.port)
            }
        return {
            "server": "{}://{}:{}".format(self.protocol, self.host, self.port),
            "username": self.username,
            "password": self.password
        }

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

    def __repr__(self):
        return self.__str__()


class HttpProxy(Proxy):
    pass


class Socks5Proxy(Proxy):
    pass
