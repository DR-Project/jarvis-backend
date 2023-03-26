import time

from typing import List
from nonebot import get_driver

from .interface import crypto_coin
from .interface import magic_usage
from .interface import rss_news
from .interface import stock
from .interface import caiyun_weather
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())


def magic_get_usage() -> str:
    try:
        lists = magic_usage.get_usage()
    except:
        ret = '接口异常'
    else:
        ret = magic_construct_string(lists)
    return ret


def magic_construct_string(lists: List[dict]) -> str:
    pattern = '%H时%M分'
    pattern2 = '%m月%d日'
    now = time.strftime(pattern, time.localtime(time.time()))
    prefix = '截至今日' + now + '\n' + '----------------\n'
    for i in lists:
        prefix += '🖥️\n' + i['node_name'] + ' 已用' + \
                  str(round(i['data_counter'] / 1024 / 1024 / 1024, 2)) + 'GiB' + \
                  '，剩余' + str(round((1 - i['data_counter'] / i['plan_monthly_data']), 2) * 100) + '%\n' + \
                  '重置时间为' + time.strftime(pattern2, time.localtime(i['data_next_reset'])) + '\n'
    prefix += '----------------\n' + '🪧 现诚招猫猫服务器 Sponsor \n有意者请与 %s 联系' % config.magic_admin_nickname
    return prefix.strip()


def coin_get_price(coin_type: str) -> str:
    instrument_id = coin_type.upper() + '-USDT'

    try:
        msg = crypto_coin.get_price(instrument_id)
        ret = crypto_coin.construct_string(msg)
    except crypto_coin.InstrumentNotExistException:
        try:
            msg_v2 = crypto_coin.get_price_instead(instrument_id)
            ret = crypto_coin.construct_string_instead(msg_v2)
        except crypto_coin.InstrumentNotExistException:
            msg_err = 'Interface Exception'
            ret = msg_err
    except crypto_coin.ReadTimeout:
        try:
            msg_v2 = crypto_coin.get_price_instead(instrument_id)
            ret = crypto_coin.construct_string_instead(msg_v2)
        except crypto_coin.InstrumentNotExistException:
            msg_err = 'Interface Exception'
            ret = msg_err
        except crypto_coin.ReadTimeout:
            msg_err = 'Interface Timeout'
            ret = msg_err
    except:
        msg_err = 'Unknown Exception'
        ret = msg_err

    return ret


def rss_get_news(target: str) -> str:
    try:
        dicts = rss_news.get_news(target, rss_news.rss_sources[target][0])
    except rss_news.RequestError:
        ret = '接口异常'
    else:
        ret = rss_news.construct_string(dicts)
    return ret


def weather_get(address: str) -> str:
    address = address[:-2].strip()

    location = caiyun_weather.get_location(address)

    line = '---------------'
    source = '以上数据来自彩云天气™️'

    if location:
        try:
            address_text = '%s%s' % (address, '' if '市' in address or '区' in address
                                                    or '省' in address else location.location_type)
            weather_text = caiyun_weather.process_weather_data(location, hourly_steps=12)
            ret = '[%s天气]%s\n%s\n%s' % (address_text, weather_text, line, source)
        except caiyun_weather.NoDefineException:
            ret = '接口异常'
    else:
        ret = '我的记忆体无法回答这个问题'
    return ret


async def get_coin_volume() -> str:
    dicts = await crypto_coin.volume_controller('24h', 6)
    ret = '🎉 Crypto Index 🎉\n\n'
    index = 1
    for i in dicts['payload']:
        if i['name'] == 'Tether':
            continue
        ret += 'No.' + str(index) + ' ' + i['name'] + ' (' + i['symbol'] + ')' + '\n'
        ret += 'Vol: ₮ ' + str(round((i['quote']['USDT']['volume_24h'] / 1000000000))) + ' Billion\n'
        ret += 'Price: ₮ ' + str(round(i['quote']['USDT']['price'], 2)) + '\n\n'
        index += 1
    return ret.strip()


async def get_stock(stock_name: str = None, stock_code: str = None):
    try:
        data = stock.stock_controller(stock_name=stock_name, stock_code=stock_code)
        ret = data[1] + '\n' + \
              '开盘：' + data[2] + '\n' + \
              '收盘：' + data[5] + '\n' + \
              '最高：' + data[5] + '\n' + \
              '涨跌幅：' + str(round(float(data[12]), 3)) + '%'
    except Exception:
        ret = 'Unknow Error'
    return ret


''' >>>>>> Exp Function <<<<<< '''


def coin_exp_get_price(instrument_id: str) -> str:
    try:
        msg = crypto_coin.get_price(instrument_id)
        ret = crypto_coin.construct_string(msg)
    except crypto_coin.InstrumentNotExistException:
        try:
            msg_v2 = crypto_coin.get_price_instead(instrument_id)
            ret = crypto_coin.construct_string_instead(msg_v2)
        except crypto_coin.InstrumentNotExistException:
            msg_err = 'Instrument 404'
            ret = msg_err
    return ret
