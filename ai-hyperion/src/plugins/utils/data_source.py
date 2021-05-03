from .interface import crypto_coin
from .interface import magic_usage
from .interface import rss_news
from .interface import weather
from .interface import assignment_ddl


def magic_get_usage() -> str:
    try:
        dicts = magic_usage.get_usage()
    except:
        ret = "接口异常"
    else:
        ret = magic_usage.construct_string(dicts)
    return ret


def coin_get_price(coin_type: str) -> str:
    instrument_id = coin_type.upper() + "-USDT"
    try:
        dicts = crypto_coin.get_price(instrument_id)
    except:
        ret = "接口异常"
    else:
        ret = crypto_coin.construct_string(dicts)
    return ret


def rss_get_news(target: str) -> str:
    try:
        dicts = rss_news.get_news(target, rss_news.rss_sources[target][0])
    except:
        ret = "接口异常"
    else:
        ret = rss_news.construct_string(dicts)
    return ret


def weather_get(city: str) -> str:
    city = city[:-2].strip()
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


def ddl_get() -> str:
    return assignment_ddl.construct_string()


''' >>>>>> Exp Function <<<<<< '''


def coin_exp_get_price(instrument_id: str) -> str:
    instrument_id = instrument_id[-8:]
    print(instrument_id)
    try:
        dicts = crypto_coin.get_price(instrument_id)
        ret = crypto_coin.construct_string(dicts)
    except:
        ret = "币对不存在"
        
    return ret
