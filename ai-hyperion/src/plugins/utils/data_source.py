import asyncio
from typing import List

from .interface import crypto_coin
from .interface import magic_usage
from .interface import rss_news
from .interface import weather
from .interface import assignment_ddl
from .interface import covid

import time


def magic_get_usage() -> str:
    try:
        lists = magic_usage.get_usage()
    except:
        ret = '接口异常'
    else:
        ret = magic_construct_string(lists)
    return ret


def magic_construct_string(lists: List[dict]) -> str:
    index = 0
    pattern = '%m月%d日 %H:%M'
    pattern2 = '%m月%d日'
    now = time.strftime(pattern, time.localtime(time.time()))
    prefix = '尊敬的***Door群客户，截至' + now + '。\n'
    for i in lists:
        prefix += '节点' + str(index) + ' 当月魔法流量已用 ' + str(round(i['data_counter'] / 1024 / 1024 / 1024, 2)) + \
                  'GiB' + '，可用 ' + str(round((1 - i['data_counter'] / i['plan_monthly_data']), 2) * 100) + '% ' + \
            '下次重置日期为' + time.strftime(pattern2, time.localtime(i['data_next_reset'])) + '。\n'
        index += 1
    return prefix


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
    data = await covid.get_china_num()
    date = data['date']
    count = data['total_vaccinations']

    new_cases = int(data['new_cases'])
    total_vaccinations_per_hundred = data['total_vaccinations_per_hundred']
    count = float(count) / 10000

    ret = '截至 ' + date + '\n\n中国内地已接种新冠疫苗 ' + str(count) + ' 万针。接种完成率为' + str(total_vaccinations_per_hundred) \
          + ' %。 \n\n' + date + ' 全国31个省级行政区和新疆生产建设宾团共报告新增确诊' + f'{new_cases}' + '人。'
    return ret


def ddl_get() -> str:
    # assignments_display = assignments[:3]

    ret = ''
    pattern = '%Y年%m月%d日 %H:%M'

    assignments = assignment_ddl.sort_assignment(
        assignment_ddl.convert_date(assignment_ddl.get_assignment(assignment_ddl.get_course())))

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


async def set_***_count(***_man: int) -> None:
    pass


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
