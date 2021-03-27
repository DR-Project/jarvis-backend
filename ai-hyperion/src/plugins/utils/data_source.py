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


def btc_get_price() -> dict:
    """

    :return: the key message to the upstream
    """

    url = 'https://www.okexcn.com/api/index/v3/BTC-USDT/constituents'

    '''
    # useless for now
    proxies = {
        # 部署到服务器或者容器里面之后 需要修改为对应的
        "http://": "http://localhost:7890",
        "https://": "http://localhost:7890",
    }
    

    r = httpx.get(url, proxies=proxies)
    '''

    r = httpx.get(url)

    payload = r.json()
    msg = {
        'okex': payload['data']['constituents'][0],
        'price': payload['data']['last']
    }

    # print(json.dumps(msg))

    return msg


def btc_construct_string(msg: dict) -> str:
    """

    :param msg:  msg is a dict from upstream method
    :return: the message that will forward to QQ
    """

    # init variable
    price = msg['price']

    # abandoned
    usd_price = msg['okex']['original_price']

    # ret = '现在BTC的价格是1BTC = ' + f'{price}' + 'USDT。折合美元价格为' + f'{usd_price}' + '刀'
    # ret = '现在BTC单位价格为 f'{price}' + 'USDT，折合美元价格为' + f'{usd_price}' + 'USD'。 
    # 这句话，你看情况改改。我不知道怎么写
    # ret = '现在BTC的价格是1 BTC = ' + f'{price}' + ' USDT。'
    # abandoned above
    ret = '现在BTC单位价格为 ' f'{price}' + ' USDT，折合美元价格为 ' + f'{usd_price}' + ' USD 。'

    return ret


mem_dicts = {
    "丢***": "***",
    "丢***": "***",
    "丢***": "***",
    "丢***": "***",
    "丢***": "***",
    "丢***": "***"
}


'''
if __name__ == '__main__':
    msg = btc_get_price()
    print(btc_construct_string(msg))
'''
