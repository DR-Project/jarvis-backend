from .interface import crypto_coin
from .interface import magic_usage
from .interface import rss_news
from .interface import weather


def magic_get_usage() -> str:
    try:
        dicts = magic_usage.get_usage()
    except:
        ret = "接口异常"
    else:
        ret = magic_usage.construct_string(dicts)
    return ret


def coin_get_price(coin_type: str) -> str:
    instrument_id = crypto_coin.cryptocurrency[coin_type]
    try:
        dicts = crypto_coin.get_price(instrument_id)
    except:
        ret = "接口异常"
    else:
        ret = crypto_coin.construct_string(dicts)
    return ret


def rss_get_news(target: str) -> str:
    try:
        dicts = rss_news.get_news(target, 8)
    except:
        ret = "接口异常"
    else:
        ret = rss_news.construct_string(dicts)
    return ret


def weather_get(city: str) -> str:
    prefix = '天气'
    city = city[:-2]
    city_list = []
    city_list.append(city)
    if weather.china_city_validator(city + '市'):
        try:
            ret = weather.get_finally_weather(city_list)
        except weather.NoDefineException:
            ret = '城市天气不存在'
        except:
            ret = '接口异常'
    else:
        ret = city + ' ∉ {城市}'
    return ret


''' >>>>>> Exp Function <<<<<< '''


def coin_exp_get_price(instrument_id: str) -> str:
    instrument_id = instrument_id[-8:]
    print(instrument_id)
    try:
        dicts = crypto_coin.get_price(instrument_id)
    except:
        ret = "币对不存在"
    else:
        ret = crypto_coin.construct_string(dicts)
    return ret
