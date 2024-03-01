import os
import typing

import webshare


def resolve(api_key: typing.Optional[str] = None) -> typing.List[str]:
    if api_key is None:
        api_key = os.environ.get("WEBSHARE_API_KEY")

    if api_key is None:
        raise Exception("WEBSHARE_API_KEY is not set")

    api_client = webshare.webshare.ApiClient(api_key)
    proxies = api_client.get_proxy_list()

    return [f"http://{p.username}:{p.password}@{p.proxy_address}:{p.port}" for p in proxies.get_results()]


if __name__ == "__main__":
    print(resolve())