from parserian.proxy import Proxy
from parserian.proxy_factory import ProxyFactory


def test_add_then_next():
    f = ProxyFactory()
    f.add(Proxy("http://1.1.1.1"))
    f.add(Proxy("http://2.2.2.2"))
    with f.next() as p:
        assert p.url == "http://1.1.1.1"
    with f.next() as p:
        assert p.url == "http://2.2.2.2"
    with f.next() as p:
        assert p.url == "http://1.1.1.1"


def test_delete():
    f = ProxyFactory()
    f.add(Proxy("http://1.1.1.1"))
    f.add(Proxy("http://2.2.2.2"))
    try:
        with f.next():
            assert f.local.proxy.url == "http://1.1.1.1"
            raise Exception("test")
    except:
        pass
    with f.next():
        assert f.proxies[0].url == "http://2.2.2.2"


def test_load_from_file():
    f = ProxyFactory()
    f.load_from_file("test_data/proxies.txt")
    assert f.proxies[0].url == 'https://192.168.0.1:8080'
    assert f.proxies[1].url == 'socks5://test.domain.com:3123'
    assert f.proxies[2].url == 'socks4://test.domain1.com:3127'
