import httpx
import json


def magic_get_usage() -> dict:
    """

    :return: the key message to upstream
    """

    url = 'https://api.64clouds.com/v1/getServiceInfo?'

    param = {
        'veid': '***',
        'api_key': '***'
    }

    r = httpx.get(url, params=param)
    # print(r.url)
    payload = r.json()
    # print(json.dumps(payload))

    # "data_next_reset" "data_counter" "plan_monthly_data" "suspended"

    msg = {
        'data_next_reset': payload['data_next_reset'],
        'data_counter': payload['data_counter'],
        'plan_monthly_data': payload['plan_monthly_data'],
        'suspended': payload['suspended']
    }

    # print(json.dumps(msg))
    return msg


def magic_construct_string(msg: dict) -> str:
    """

    :param msg: msg is a dict from upstream method
    :return: the message that will forward to QQ
    """

    # init variable
    data_usage = (msg['data_counter'] / 1024 / 1024 / 1024)
    data_usage = round(data_usage, 2)
    plan_monthly_data = (msg['plan_monthly_data'] / 1024 / 1024 / 1024)
    plan_monthly_data = round(plan_monthly_data, 2)

    # TODO
    suspended = msg['suspended']
    data_next_reset = msg['data_next_reset']

    left_data = plan_monthly_data - data_usage
    left_data = round(left_data, 2)
    ret = '本月魔法剩余' + f'{left_data}' + ' GB, 已经使用 ' + f'{data_usage}' + ' GB.'

    return ret


def get_price(instrument_id: str) -> dict:
    """
    :param instrument_id: the cryptocurrency you want to check
    :return: the key message to the upstream
    """

    url = 'https://www.okexcn.com/api/spot/v3/instruments/' + f'{instrument_id}' + '/ticker'

    '''
    # useless for now
    proxies = {
        # 部署到服务器或者容器里面之后 需要修改为对应的
        'http://': "http://localhost:7890',
        'https://': "http://localhost:7890',
    }

    r = httpx.get(url, proxies=proxies)
    '''

    r = httpx.get(url)

    # payload = r.json()

    '''msg = {
        'okex': payload['data']['constituents'][0],
        'price': payload['data']['last']
    }'''
    msg = r.json()
    # print(json.dumps(msg))

    return msg


def construct_string(msg: dict) -> str:
    """

    :param msg:  msg is a dict from upstream method
    :return: the message that will forward to QQ
    """

    # init variable
    price = msg['last']
    product_id = msg['product_id']

    coin = product_id.split('-')[0]
    # print(tmp)

    ret = '现在' + f'{coin}' + '的价格是1 ' + f'{coin}' + ' = ' + f'{price}' + ' USDT。'
    # abandoned
    # ret = '现在BTC单位价格为 ' f'{price}' + ' USDT，折合美元价格为 ' + f'{usd_price}' + ' USD 。'

    return ret


mem_dicts = {
    "丢***": "***",
    "丢***": "***",
    "丢***": "***",
    "丢***": "***",
    "丢***": "***",
    "丢***": "***"
}

cryptocurrency = {
    'BTC': 'BTC-USDT',
    'EOS': 'EOS-USDT',
    'BTG': 'BTG-USDT',
    'ADA': 'ADA-USDT',
    'DOGE': 'DOGE-USDT',
    'LTC': 'LTC-USDT',
    'ETH': 'ETH-USDT'
}


if __name__ == '__main__':
    msg = get_price('BTC-USDT')
    print(construct_string(msg))

