import httpx
import json


def get_price(instrument_id: str) -> dict:
    """
    :param instrument_id: the cryptocurrency you want to check
    :return: the key message to the upstream
    """

    url = 'https://www.okexcn.com/api/spot/v3/instruments/' + f'{instrument_id}' + '/ticker'

    # for test to raise Exception
    # url = 'www.test404domain.cc'

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
        msg = r.json()
    # payload = r.json()

    '''msg = {
        'okex': payload['data']['constituents'][0],
        'price': payload['data']['last']
    }'''
    # print(json.dumps(msg))

    return msg


def construct_string(msg: dict) -> str:
    """

    :param msg:  msg is a dict from upstream method
    :return: the message that will forward to QQ
    """

    # init variable
    price = float(msg['last'])
    product_id = msg['product_id']
    open_utc8 = float(msg['open_utc8'])
    change_percent = round((price - open_utc8) / price * 100, 2)

    instrument_id = product_id.split('-')
    coin = instrument_id[0]
    base = instrument_id[1]
    # print(change_percent)

    ret = '现在' + f'{coin}' + '的价格是1 ' + f'{coin}' + ' = ' + f'{price}' + ' ' + f'{base}' + '，对比今天开盘价涨幅为 ' \
          + f'{change_percent}' + '%。 '
    # abandoned
    # ret = '现在BTC单位价格为 ' f'{price}' + ' USDT，折合美元价格为 ' + f'{usd_price}' + ' USD 。'

    return ret


cryptocurrency = {
    'BTC': 'BTC-USDT',
    'EOS': 'EOS-USDT',
    'BTG': 'BTG-USDT',
    'ADA': 'ADA-USDT',
    'DOGE': 'DOGE-USDT',
    'LTC': 'LTC-USDT',
    'ETH': 'ETH-USDT'
}
