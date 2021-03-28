import httpx

def get_colorful() -> dict:

    url = 'https://api.lolicon.app/setu/'

    param = {
        'r18': '0',
        'size1200' : 'true'
    }

    proxies = {
            'http://': 'http://localhost:7890',
            'https://': 'http://localhost:7890'
        }

    r = httpx.get(url, params=param, proxies=proxies)
    
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