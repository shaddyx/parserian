# A bunch of tools for parsing/scraping

## Proxy factory

The proxy factory is the tool to rotate proxies using the round robin algo

Example usage:
```python
import parserian.proxy_factory as pf
import parserian.proxy as proxy
f = pf.ProxyFactory()
f.add(proxy.Proxy("http://1.1.1.1"))
f.add(proxy.Proxy("http://2.2.2.2"))
with f.next() as p:
    assert p.url == "http://1.1.1.1:80"
with f.next() as p:
    assert p.url == "http://2.2.2.2:80"
with f.next() as p:
    assert p.url == "http://1.1.1.1:80"
```

The code will automatically delete incorrect proxy from the list if some error happened 
(for now the main policy is to delete proxies after any error, other policies will be added in the future)


```python
import parserian.proxy_factory as pf
import parserian.proxy as proxy
f = pf.ProxyFactory()
f.add(proxy.Proxy("http://1.1.1.1"))
f.add(proxy.Proxy("http://2.2.2.2"))
try:
    with f.next() as p:
        assert p.url == "http://1.1.1.1:80"
        raise Exception("test")
except:
    pass
with f.next():
    assert f.proxies[0].url == "http://2.2.2.2:80"
```
## Proxy rotation strategy

The idea is to have different rotation strategies for proxies, the following strategies implemented:

### Round robin

the strategy will take proxies one by one using the same order in which they were added to the proxy factory 

```python
import parserian.proxy_factory as pf
import parserian.proxy as proxy
from parserian import proxy_rotation_strategy as proxy_strategy
f = pf.ProxyFactory()
f.strategy = proxy_strategy.RoundRobinProxyStrategy(track_usage=True, cool_down=0.1)
```

### Random

the strategy will take a random proxy from the list

```python
import parserian.proxy_factory as pf
import parserian.proxy as proxy
from parserian import proxy_rotation_strategy as proxy_strategy
f = pf.ProxyFactory()
f.strategy = proxy_strategy.RoundRobinProxyStrategy(track_usage=True, cool_down=0.1)
```


