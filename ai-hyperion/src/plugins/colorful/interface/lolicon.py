import os
import json
import httpx
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


def construct_string(msg: dict) -> str:
    msg = msg['data'][0]
    url = msg['url']
    pid = 'PID: ' + str(msg['pid']) + '\n'
    title = '标题: ' + msg['title'] + '\n'
    author = '作者: ' + msg['author'] + '\n'
    ret = [{
            'type': 'text',
            'data': {
                'text': pid
            }
        }, {
            'type': 'text',
            'data': {
                'text': title
            }
        }, {
            'type': 'text',
            'data': {
                'text': author
            }
        }, {
            'type': 'image',
            'data': {
                'file': url
            }
        }]
    return ret
