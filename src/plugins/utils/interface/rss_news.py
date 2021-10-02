from typing import List

import httpx
import json
import xmltodict
import time


class RequestError(Exception):
    pass


def get_news(target: str, quantity: int) -> dict:
    """

    :param target: rss target, the url must fit rss v2.0 standard
    :param quantity: to control how many news wants to return
    :return: the top 5 news from rss_source
    """
    # url = 'https://a.jiemian.com/index.php?m=article&a=rss'

    # rss_source = rss_sources[rss_source]

    proxies = {
            # 部署到服务器或者容器里面之后 需要修改为对应的
            'http://': 'http://localhost:7890',
            'https://': 'http://localhost:7890'
        }

    try:
        r = httpx.get(rss_sources[target][1], proxies=proxies)
    except httpx.RequestError:
        raise RequestError('Interface Error / 接口异常')
    else:
        xml = xmltodict.parse(r.text)
        payload = json.loads(json.dumps(xml))

        msg = {}
        item = []
        for i in range(quantity):
            item.append(payload['rss']['channel']['item'][i])

        msg['item'] = item
        msg['target'] = target
        return msg


def construct_string(msg: dict) -> str:
    """
    :param msg:  msg is a dict from upstream method
    :return: the message that will forward to QQ
    """

    # init variable
    target = msg['target']
    date = time.strftime('%m月%d日', time.localtime())
    ret = date + ' ' + target + '\n\n'
    num = 0

    for item in msg['item']:
        title = item['title']
        # link = item['link']
        num_hex = '0x{:02X}'.format(num)
        ret += f'{num_hex}' + '. ' + f'{title}' + '\n\n'
        num += 1

    return ret[:-2]


rss_sources = {
    '药闻': [8, 'https://a.jiemian.com/index.php?m=article&a=rss'],
    '热搜': [15, 'https://rsshub.app/weibo/search/hot'],
    'TESTNEWS': [10, 'https://rsshub.app/thepaper/featured']
}


# if __name__ == '__main__':
#     msg = get_news('药闻', 5)
#     print(construct_string(msg))

