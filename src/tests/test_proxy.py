from parserian.proxy import Proxy


def test_proxy():
    p = Proxy("1.1.1.1:8008")
    assert p.url == "http://1.1.1.1:8008"
    assert p.host == "1.1.1.1"
    assert p.port == 8008


    p = Proxy("http://1.1.1.1")
    assert p.url == "http://1.1.1.1:80"
    assert p.port == 80
    assert p.protocol == "http"
    assert p.host == "1.1.1.1"

    p = Proxy("http://1.1.1.1:8080")
    assert p.url == "http://1.1.1.1:8080"
    assert p.port == 8080
    assert p.protocol == "http"

    p = Proxy("https://testuser:testpass@1.1.1.1")
    assert p.url == "https://testuser:testpass@1.1.1.1:80"
    assert p.username == "testuser"
    assert p.password == "testpass"
    assert p.port == 80
    assert p.protocol == "https"
    assert p.host == "1.1.1.1"


def test_proxy_error():
    try:
        p = Proxy("http:/")
        assert False
    except:
        pass


