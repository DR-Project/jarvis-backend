import os
import httpx
import json, base64
from typing import List


def get_lolicon() -> dict:
    """

    :return: msg is a dict from upstream method
    """
    url = 'https://api.lolicon.app/setu/'

    param = {
        'apikey': '***',
        'r18': '0',
        'size1200': True,
    }

    proxies = {
        'http://': 'http://localhost:7890',
        'https://': 'http://localhost:7890'
    }

    try:
        r = httpx.get(url, params=param, proxies=proxies)

    except httpx.RequestError:

        raise Exception('Interface Error / 接口异常')

    else:

        payload = r.json()

    msg = {
        'code': payload['code'],
        'msg': payload['msg'],
        'quota': payload['quota'],
        'quota_min_ttl': payload['quota_min_ttl'],
        'count': payload['count'],
        'data': payload['data']
    }

    return msg


def dump_img(url: str) -> bytes:

    proxies = {
        'http://': 'http://localhost:7890',
        'https://': 'http://localhost:7890'
    }

    try:
        r = httpx.get(url, proxies=proxies)
    except httpx.RequestError:
        raise Exception('接口异常')

    ret = r.content

    return ret

def convert_base64(bitstream: bytes) -> str:
    ret = str(base64.b64encode(bitstream).decode('UTF-8'))
    return ret
