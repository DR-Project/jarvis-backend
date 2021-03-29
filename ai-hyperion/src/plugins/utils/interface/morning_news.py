import httpx
import json
import xmltodict


def get_news(rss_source: str) -> list:
    """

    :return: the top 5 news from ithome
    """

    url = 'https://a.jiemian.com/index.php?m=article&a=rss'

    proxies = {
            # 部署到服务器或者容器里面之后 需要修改为对应的
            'http://': 'http://localhost:7890',
            'https://': 'http://localhost:7890'
        }

    try:
        r = httpx.get(url, proxies=proxies)
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
    """

    :param msg:  msg is a dict from upstream method
    :return: the message that will forward to QQ
    """

    # init variable
    ret = ''
    num = 0
    for item in msg:
        title = item['title']
        link = item['link']
        num_hex = '0x{:02X}'.format(num)
        ret += f'{num_hex}' + '. ' + f'{title}' + '\n' + f'{link}' + '\n\n'
        num += 1

    return ret


'''
if __name__ == '__main__':
    msg = get_news()
    print(construct_string(msg))
'''
