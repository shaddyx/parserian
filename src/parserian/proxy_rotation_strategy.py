import abc
import random
import time


class ProxyStrategy:
    from parserian.proxy import Proxy
    from parserian.proxy_factory import ProxyFactory

    def __init__(self, cool_down: float = None, track_usage: bool = False):
        """
        Proxy Rotation Strategy
            :param float cool_down:  - if enabled will only return an available proxy after cool_down seconds
            :param bool track_usage: - if enabled will track usage of proxy and will prevent returning an unavailable proxy
        """
        self.cool_down = cool_down
        self.track_usage = track_usage

    @abc.abstractmethod
    def next(self, proxy_factory: ProxyFactory) -> Proxy:
        """
        Returns the next available proxy
        :param proxy_factory: should receive a ProxyFactory instance
        :return: returns next available proxy
        """
        raise NotImplementedError

    def _check_availability(self, proxy):
        return (not proxy.acquired or not self.track_usage) and (
                self.cool_down is None or
                self.cool_down < time.time() - proxy.last_used_time
        )


class ProxyNotAvailableException(Exception):
    pass


class RoundRobinProxyStrategy(ProxyStrategy):
    from parserian.proxy import Proxy
    from parserian.proxy_factory import ProxyFactory

    def __init__(self, cool_down: float = None, track_usage: bool = False):
        super().__init__(cool_down, track_usage)

    def next(self, proxy_factory: ProxyFactory) -> Proxy:
        with proxy_factory.lock:
            if proxy_factory.index >= len(proxy_factory.proxies):
                proxy_factory.index = 0

            index: int = self.find_next_available(proxy_factory)
            proxy = proxy_factory.proxies[index]
            proxy_factory.index = index + 1
            return proxy


    def find_next_available(self, proxy_factory: ProxyFactory):
        iteration_counter = 0
        index = proxy_factory.index
        while True:
            iteration_counter += 1
            if index >= len(proxy_factory.proxies):
                index = 0
            if self._check_availability(proxy_factory.proxies[index]):
                return index
            if iteration_counter > len(proxy_factory.proxies):
                raise ProxyNotAvailableException("Could not find an available proxy")
            index += 1


class RandomProxyStrategy(ProxyStrategy):
    from parserian.proxy import Proxy
    from parserian.proxy_factory import ProxyFactory

    def __init__(self, cool_down: float = None, track_usage: bool = False):
        super().__init__(cool_down, track_usage)

    def next(self, proxy_factory: ProxyFactory) -> Proxy:
        checked = set()
        with proxy_factory.lock:
            while True:
                proxy_factory.index = random.randint(0, len(proxy_factory.proxies) - 1)
                proxy = proxy_factory.proxies[proxy_factory.index]
                if proxy not in checked:
                    checked.add(proxy)
                if self._check_availability(proxy):
                    return proxy
                if len(checked) == len(proxy_factory.proxies):
                    raise ProxyNotAvailableException("Could not find an available proxy")
