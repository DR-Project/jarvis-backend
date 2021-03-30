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
    city_py = weather.get_pinyin_list(city_list)
    try:
        ret = weather.particular_time_construct_string(city_py)
    except:
        ret = "接口异常"
    return ret
