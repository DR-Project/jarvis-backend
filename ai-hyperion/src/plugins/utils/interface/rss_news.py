import httpx
import json
import xmltodict
import time


def get_news(rss_source: str, quantity: int) -> list:
    """

    :param rss_source: rss url, must fit rss v2.0 standard
    :param quantity: to control how many news wants to return
    :return: the top 5 news from rss_source
    """
    # url = 'https://a.jiemian.com/index.php?m=article&a=rss'

    rss_source = rss_sources[rss_source]

    proxies = {
            # 部署到服务器或者容器里面之后 需要修改为对应的
            'http://': 'http://localhost:7890',
            'https://': 'http://localhost:7890'
        }

    try:
        r = httpx.get(rss_source, proxies=proxies)
    except httpx.RequestError:
        raise Exception('Interface Error / 接口异常')
    else:
        xml = xmltodict.parse(r.text)
        payload = json.loads(json.dumps(xml))

        msg = []

        for i in range(quantity):
            msg.append(payload['rss']['channel']['item'][i])
        # print(msg)
        return msg


def construct_string(msg: dict, target: str) -> str:
    """

    :param msg:  msg is a dict from upstream method
    :return: the message that will forward to QQ
    """

    # init variable
    date = time.strftime('%m月%d日', time.localtime())
    ret = date + ' ' + target + '\n\n'
    num = 0

    # print(type(date))

    for item in msg:
        title = item['title']
        link = item['link']
        num_hex = '0x{:02X}'.format(num)
        ret += f'{num_hex}' + '. ' + f'{title}' + '\n' + '\n'
        num += 1

    return ret


rss_sources = {
    '药闻': 'https://a.jiemian.com/index.php?m=article&a=rss',
    '热搜': 'https://rsshub.app/weibo/search/hot'
}


if __name__ == '__main__':
    msg = get_news('https://a.jiemian.com/index.php?m=article&a=rss', 5)
    print(construct_string(msg))

