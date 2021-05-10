from .interface import crypto_coin
from .interface import magic_usage
from .interface import rss_news
from .interface import weather
from .interface import assignment_ddl
from .interface import covid_vaccinations

import time


def magic_get_usage() -> str:
    try:
        dicts = magic_usage.get_usage()
    except:
        ret = '接口异常'
    else:
        ret = magic_usage.construct_string(dicts)
    return ret


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
    return ret


def rss_get_news(target: str) -> str:
    try:
        dicts = rss_news.get_news(target, rss_news.rss_sources[target][0])
    except:
        ret = '接口异常'
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


async def covid_get_vaccinations():
    data = await covid_vaccinations.get_last_date()
    date = data['date']
    count = data['total_vaccinations']
    count = float(count) / 10000
    pattern = '%Y-%m-%d'
    date = time.strftime(pattern, time.localtime(date))
    ret = '截至 ' + date + ' 中国内地已接种' + str(count) + '万针'
    return ret


def ddl_get() -> str:
        # assignments_display = assignments[:3]

    ret = ''
    pattern = '%Y年%m月%d日 %H:%M'

    assignments = assignment_ddl.sort_assignment(assignment_ddl.convert_date(assignment_ddl.get_assignment(assignment_ddl.get_course())))

    for assignment in assignments:
        # init variable
        course_name = assignment['course_name']
        course_code = assignment['course_code']
        deadline = assignment['ddl']
        assignment_name = assignment['name']

        ddl = time.strftime(pattern, time.localtime(deadline))
        now = time.time()

        if now <= deadline:
            ret += f'{course_code}' + ' ' + f'{course_name}' + ' ' + f'{assignment_name}' + '\n' \
                   + f'{ddl}' + '\n\n'

    return ret[:-2]


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
