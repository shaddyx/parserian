import os
import time

from parserian import proxy_rotation_strategy as proxy_strategy
from parserian.proxy import Proxy
from parserian.proxy_factory import ProxyFactory

curdir = os.path.dirname(os.path.abspath(__file__))


def test_add_then_next():
    f = ProxyFactory()
    f.add(Proxy("http://1.1.1.1"))
    f.add(Proxy("http://2.2.2.2"))
    with f.next() as p:
        assert p.url == "http://1.1.1.1:80"
    with f.next() as p:
        assert p.url == "http://2.2.2.2:80"
    with f.next() as p:
        assert p.url == "http://1.1.1.1:80"


def test_add_the_same():
    f = ProxyFactory()
    f.add(Proxy("http://1.1.1.1"))
    f.add(Proxy("http://1.1.1.1"))
    assert len(f.proxies) == 1


def test_round_robin_with_tracking():
    f = ProxyFactory()
    f.strategy = proxy_strategy.RoundRobinProxyStrategy(track_usage=True, cool_down=0.1)
    f.add(Proxy("http://1.1.1.1"))
    f.add(Proxy("http://2.2.2.2"))

    with f.next() as p:
        assert p.url == "http://1.1.1.1:80"
    with f.next() as p:
        assert p.url == "http://2.2.2.2:80"
    time.sleep(0.1)
    with f.next() as p:
        assert p.url == "http://1.1.1.1:80"
    with f.next() as p:
        assert p.url == "http://2.2.2.2:80"
    try:
        with f.next() as p:
            assert False, "Should be an error"
    except proxy_strategy.ProxyNotAvailableException:
        pass


def test_delete():
    f = ProxyFactory()
    f.add(Proxy("http://1.1.1.1"))
    f.add(Proxy("http://2.2.2.2"))
    try:
        with f.next() as p:
            assert p.url == "http://1.1.1.1:80"
            raise Exception("test")
    except:
        pass
    with f.next():
        assert f.proxies[0].url == "http://2.2.2.2:80"


def test_load_from_file():
    f = ProxyFactory()
    f.load_from_file(curdir + "/test_data/proxies.txt")
    assert f.proxies[0].url == 'https://192.168.0.1:8080'
    assert f.proxies[1].url == 'socks5://test.domain.com:3123'
    assert f.proxies[2].url == 'socks4://test.domain1.com:3127'


def test_random_strategy():
    f = ProxyFactory()
    f.add(Proxy("http://1.1.1.1"))
    f.add(Proxy("http://2.2.2.2"))
    f.add(Proxy("http://3.3.3.3"))
    f.strategy = proxy_strategy.RandomProxyStrategy()
    last = None
    found = False
    elements = []
    for i in range(100):
        with f.next() as p:
            assert p.url in ["http://1.1.1.1:80", "http://2.2.2.2:80", "http://3.3.3.3:80"]
            if last is not None:
                if last != p.url:
                    found = True
            last = p.url
            elements.append(p.url)
    assert found

    assert len(list(set(elements))) == 3


def test_random_strategy_cooldown():
    f = ProxyFactory()
    f.strategy = proxy_strategy.RandomProxyStrategy(cool_down=0.1, track_usage=True)
    f.add(Proxy("http://1.1.1.1"))
    f.add(Proxy("http://2.2.2.2"))
    with f.next() as p:
        assert p.url in ["http://1.1.1.1:80", "http://2.2.2.2:80"]
    with f.next() as p:
        assert p.url in ["http://1.1.1.1:80", "http://2.2.2.2:80"]

    try:
        with f.next() as p:
            assert False, "Should be an error"
    except proxy_strategy.ProxyNotAvailableException:
        pass
