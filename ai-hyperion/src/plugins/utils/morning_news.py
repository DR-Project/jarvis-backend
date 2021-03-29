import httpx
import json
import xmltodict


def get_news() -> list:

    url = 'https://www.ithome.com/rss/'

    try:
        r = httpx.get(url)
    except httpx.RequestError:
        raise Exception('Interface Error / 接口异常')
    else:
        xml = xmltodict.parse(r.text)
        payload = json.loads(json.dumps(xml))

        msg = []

        for i in range(5):
            msg.append(payload['rss']['channel']['item'][i])
        # print(msg)
        return msg


def construct_string(msg: dict) -> str:
    ret = ''
    num = 0
    for item in msg:
        title = item['title']
        link = item['link']

        ret += f'{hex(num)}' + '.' + f'{title}' + '\n' + f'{link}' + '\n\n'
        num += 1

    return ret


if __name__ == '__main__':
    msg = get_news()
    print(construct_string(msg))
