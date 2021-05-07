import asyncio

import httpx
import json


class InstrumentNotExistException(Exception):
    """
    defined a InstrumentNotExist Exception
    """
    pass


class RequestError(Exception):
    pass


class ReadTimeout(Exception):
    pass


class NoDefineException(Exception):
    """
    defined a NoDefineException
    """
    pass


def get_price(instrument_id: str) -> dict:
    """
    :param instrument_id: the cryptocurrency you want to check
    :return: the key message to the upstream
    """

    url = 'https://www.okex.win/api/spot/v3/instruments/' + f'{instrument_id}' + '/ticker'

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

    if 'last' not in msg:
        raise InstrumentNotExistException('币对不存在')

    # init variable
    price = float(msg['last'])
    product_id = msg['product_id']
    open_utc8 = float(msg['open_utc8'])
    change_percent = round((price - open_utc8) / open_utc8 * 100, 2)

    instrument_id = product_id.split('-')
    coin = instrument_id[0]
    base = instrument_id[1]
    # print(change_percent)

    ret = '现在' + f'{coin}' + '的价格是1 ' + f'{coin}' + ' = ' + f'{price}' + ' ' + f'{base}' + '，对比今天开盘价涨幅为 ' \
          + f'{change_percent}' + '%。 '
    # abandoned
    # ret = '现在BTC单位价格为 ' f'{price}' + ' USDT，折合美元价格为 ' + f'{usd_price}' + ' USD 。'

    return ret


'''
👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇
👇👇**Basic Plan:                               👇👇
👇👇                                            👇👇
👇👇Daily credit limit: 333 (soft cap)          👇👇
👇👇Monthly credit limit: 10,000 (hard cap)     👇👇
👇👇                                            👇👇
👇👇API call rate limit: 30 requests a minute   👇👇
👇👇Endpoints enabled: 9                        👇👇
👇👇Currency conversions: Limit 1 per request   👇👇
👇👇License: Personal use                       👇👇
👇👇                                            👇👇
👇👇You are currently on a basic free plan.     👇👇
👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇
'''


def get_price_instead(instrument_id: str) -> dict:

    host = 'pro-api.coinmarketcap.com'
    endpoint = '/v1/cryptocurrency/quotes/latest'
    url = 'https://' + host + endpoint

    proxies = {
        # 部署到服务器或者容器里面之后 需要修改为对应的
        'http://': 'http://localhost:7890',
        'https://': 'http://localhost:7890'
    }

    headers = {
        'Accept': 'application / json',
        'X-CMC_PRO_API_KEY': '***'
    }
    request_data = instrument_id.split('-')
    symbol = request_data[0]
    convert = request_data[1]

    params = {
        'symbol': symbol,
        'convert': convert
    }

    try:
        r = httpx.get(url, params=params, proxies=proxies, headers=headers)
    except httpx.RequestError:
        raise RequestError('Request Error')
    except httpx.ReadTimeout:
        raise ReadTimeout('Read Timeout')
    else:
        msg = r.json()

    print(msg)
    payload = {}
    try:
        if msg['status']['error_code'] == 0:
            payload['coin'] = symbol
            payload['price'] = msg['data'][symbol]['quote'][convert]['price']
            payload['base'] = convert
            payload['change_percent'] = msg['data'][symbol]['quote'][convert]['percent_change_24h']
        else:
            raise NoDefineException('返回体不正确')
    except KeyError:
        raise NoDefineException('未定义异常 （确信')

    return payload


def construct_string_instead(payload: dict) -> str:

    # init variable
    coin = payload['coin']
    base = payload['base']
    last = payload['price']
    change_percent = payload['change_percent']

    ret = '现在' + f'{coin}' + '的价格是1 ' + f'{coin}' + ' = ' + f'{last}' + ' ' + f'{base}' + '，24小时涨幅为 ' \
          + f'{change_percent}' + '%。 '

    return ret


def set_line() -> any:
    # todo
    pass


def auto_alert() -> any:
    # todo
    pass


'''
👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇
👇👇**Basic Plan:                               👇👇
👇👇                                            👇👇
👇👇Daily credit limit: 333 (soft cap)          👇👇
👇👇Monthly credit limit: 10,000 (hard cap)     👇👇
👇👇                                            👇👇
👇👇API call rate limit: 30 requests a minute   👇👇
👇👇Endpoints enabled: 9                        👇👇
👇👇Currency conversions: Limit 1 per request   👇👇
👇👇License: Personal use                       👇👇
👇👇                                            👇👇
👇👇You are currently on a basic free plan.     👇👇
👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇
'''


async def get_market_capitalization() -> str:
    API_KEY = '***'

    host = 'https://pro-api.coinmarketcap.com'
    endpoint = '/v1/cryptocurrency/listings/latest'
    url = host + endpoint

    proxies = {
        # 部署到服务器或者容器里面之后 需要修改为对应的
        'http://': 'http://localhost:7890',
        'https://': 'http://localhost:7890'
    }

    headers = {
        'Accept': 'application / json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    async with httpx.AsyncClient(proxies=proxies, headers=headers) as client:
        try:
            r = await client.get(url)
        except httpx.RequestError:
            raise RequestError('Request Error')
        except httpx.ReadTimeout:
            raise ReadTimeout('Read Timeout')
        else:
            msg = r.text

    return msg


async def process_data() -> dict:
    """

    :return: a dict.

    the object contains two things,
        one is a timestamp (ISO 8601) on the server,
        another is a json array, which contains 10 objects
            each object contains the information about the crypto asset in Descending order

    You probably only needs the timestamp(or last_updated), symbol, market_cap

    template :
    {
        "timestamp": "2021-05-06T07:33:00.176Z",
        "payload": [
            {
                "id": 1, // id doesnt mean anything
                "name": "Bitcoin",
                "symbol": "BTC",
                "slug": "bitcoin",
                "num_market_pairs": 9513,
                "date_added": "2013-04-28T00:00:00.000Z",
                "tags": [29 items],
                "max_supply": 21000000,
                "circulating_supply": 18701106,
                "total_supply": 18701106,
                "platform": null,
                "cmc_rank": 1,
                "last_updated": "2021-05-06T07:32:02.000Z",
                "quote": {
                    "USD": {
                        "price": 56776.252502255695,
                        "volume_24h": 67733917594.070595,
                        "percent_change_1h": -0.17821812,
                        "percent_change_24h": 4.02751912,
                        "percent_change_7d": 4.27689177,
                        "percent_change_30d": -3.57890923,
                        "percent_change_60d": 14.44680101,
                        "percent_change_90d": 51.03463704,
                        "market_cap": 1061778716327.449, //should change the unit to human readable
                        "last_updated": "2021-05-06T07:32:02.000Z"
                    }
                }
            },
        ]
    }

    """

    data = json.loads(await get_market_capitalization())

    ret = {}

    if data['status']['error_code'] != 0:
        raise RequestError('Request Error')
    else:
        ret['timestamp'] = data['status']['timestamp']
        ret['payload'] = data['data'][:10]

    return ret


async def market_capitalization_controller() -> dict:
    """
    *** It's a controller method to call
        to check the object template in process_data() method
        You need to call it to get the dict and construct the string by your own.

    :return: dict
    """
    ret = await process_data()

    return ret


if __name__ == '__main__':

    instrument_id = 'SHIB-BTC'

    try:
        msg = get_price(instrument_id)
        construct_string(msg)
    except InstrumentNotExistException:
        msg_v2 = get_price_instead(instrument_id)
        ret = construct_string_instead(msg_v2)
        print(ret)


