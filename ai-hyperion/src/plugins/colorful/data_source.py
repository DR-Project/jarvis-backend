import httpx


def get_colorful() -> dict:
    """

    :return: msg is a dict from upstream method
    """
    url = 'https://api.lolicon.app/setu/'

    param = {
        'r18': '0',
        'size1200': True
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


if __name__ == '__main__':
    msg = get_colorful()['data'][0]
    print('PID: ' + str(msg['pid']))
