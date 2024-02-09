import abc
import random

class ProxyStrategy:
    from parserian.proxy import Proxy
    from parserian.proxy_factory import ProxyFactory

    @abc.abstractmethod
    def next(self, proxy_factory: ProxyFactory) -> Proxy:
        raise NotImplementedError


class RoundRobinProxyStrategy(ProxyStrategy):
    from parserian.proxy import Proxy
    from parserian.proxy_factory import ProxyFactory

    def next(self, proxy_factory: ProxyFactory) -> Proxy:
        with proxy_factory.lock:
            if proxy_factory.index >= len(proxy_factory.proxies):
                proxy_factory.index = 0

            proxy = proxy_factory.proxies[proxy_factory.index]
            proxy_factory.index += 1
            return proxy


class RandomProxyStrategy(ProxyStrategy):
    from parserian.proxy import Proxy
    from parserian.proxy_factory import ProxyFactory

    def next(self, proxy_factory: ProxyFactory) -> Proxy:
        with proxy_factory.lock:
            proxy_factory.index = random.randint(0, len(proxy_factory.proxies) - 1)
            proxy = proxy_factory.proxies[proxy_factory.index]
            return proxy
