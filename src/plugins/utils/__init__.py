import datetime
import json
import random

import nonebot
import asyncio
import re

from nonebot.rule import Rule
from nonebot.typing import T_State

from .config import Config
from nonebot import get_driver, require, logger
from nonebot.plugin import on_regex, on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Event, Message

from . import data_source
from .interface.caiyun_weather import process_weather_data, Location
from .interface.chinese_holiday import is_public_holiday, Holiday
from .interface.currency import get_rate

global_config = get_driver().config
config = Config(**global_config.dict())
driver = nonebot.get_driver()
scheduler = require('nonebot_plugin_apscheduler').scheduler

# Constant List

REG_TRAFFIC = '^(查流量|魔法|Magic|CXLL)$'
REG_COIN = '^(BTC|EOS|BTG|ADA|DOGE|LTC|ETH|' + \
           'BCH|BSV|DOT|ATOM|UNI|ZEC|SUSHI|DASH|OKB|OKT|' + \
           'BTT|FLOW|AE|SHIB|BCD|NANO|WAVES|XCH|TRX|JWT|WIN)\**([0-9]*)*$'
REG_HOTCOIN = '(热门货币|hotcoin)'
REG_NEWS = '^(药闻|热搜|TESTNEWS)$'
REG_WEATHER = '^.+(天气)$'
REG_DDL = '^(DDL)$'
EREG_COIN = 'ECOIN'
STOCK = 'STOCK'

# Register Event

traffic = on_regex(REG_TRAFFIC, re.IGNORECASE)
cryptocoin = on_regex(REG_COIN, re.IGNORECASE)
hotcoin = on_regex(REG_HOTCOIN)
mars_news = on_regex(REG_NEWS)
weather = on_regex(REG_WEATHER)
ass_ddl = on_regex(REG_DDL, re.IGNORECASE)
exp_cryptocoin = on_command(EREG_COIN)
stock = on_command(STOCK)


# rule checker
def weather_condition_checker():
    async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
        """
        自定义规则检查器
        1. 是一个 回复 消息
        2. 原消息是一个小程序
        3. 小程序是一个地图 且该地图是 腾讯地图
        4. 消息的正文中出现 天气 两个字
        """
        if hasattr(event, 'reply'):
            # 在这个位置写入你的判断代码
            if '天气' == event.get_plaintext():
                _ = [x for x in event.reply.message if x.type == 'json'][0]
                message = _.get('data').get('data')
                data = json.loads(message)
                if data.get('app') == 'com.tencent.map':
                    return True
    return Rule(_checker)
# rule checker


xxx = on_message(rule=weather_condition_checker())

''' >>>>>> Core Function for Utils <<<<<< '''


@traffic.handle()
async def _traffic(bot: Bot, event: MessageEvent):
    ret = data_source.magic_get_usage()
    await bot.send(event, ret, at_sender=False)


@cryptocoin.handle()
async def _cryptocoin(bot: Bot, event: MessageEvent):
    message = event.get_plaintext()
    if message.count('*') > 1:
        await bot.send(event, '语法错误', at_sender=False)
        return

    if '*' not in message:
        coin_type = message.upper()
        ret = data_source.coin_get_price(coin_type)
        await bot.send(event, ret, at_sender=False)

    else:
        coin_type, loop_times = message.split('*')

        if not loop_times.isnumeric():
            await bot.send(event, '语法错误', at_sender=False)
            return

        loop_times = int(loop_times)

        if loop_times < 1:
            await bot.send(event, '语法错误', at_sender=False)
            return

        if loop_times > 8:
            await bot.send(event, '复读次数过多，会被封号 ', at_sender=False)
            return

        for _ in range(loop_times):
            coin_type = coin_type.upper()
            ret = data_source.coin_get_price(coin_type)
            await bot.send(event, ret, at_sender=False)
            if _ != loop_times - 1:
                await asyncio.sleep(30)


@mars_news.handle()
async def _mars_news(bot: Bot, event: MessageEvent):
    target = event.get_plaintext()
    ret = data_source.rss_get_news(target)
    await bot.send(event, ret, at_sender=False)


@weather.handle()
async def _weather(bot: Bot, event: MessageEvent):
    target = event.get_plaintext()
    ret = data_source.weather_get(target)
    await bot.send(event, ret, at_sender=False)


@ass_ddl.handle()
async def _ass_ddl(bot: Bot, event: MessageEvent):
    await bot.send(event, '此功能已下线', at_sender=False)


@xxx.handle()
async def _xxx(bot: Bot, event: MessageEvent):
    reply = event.reply
    if not reply:
        logger.info('reply is empty')
        return

    json_message = reply.message[1].get('data').get('data')
    location = json.loads(json_message).get('meta').get('Location.Search')
    logger.debug(location)

    location_object = Location(location.get('lat'), location.get('lng'))

    line = '---------------'
    source = '以上数据来自彩云天气™️'

    weather_message = Message({
        'type': 'text',
        'data': {
            'text': '\n%s\n%s\n%s' % (process_weather_data(location_object, hourly_steps=4),
                                      line, source)
        }
    })

    await xxx.finish(weather_message, at_sender=True)


@hotcoin.handle()
async def hotcoin(bot: Bot, event: MessageEvent):
    ret = await data_source.get_coin_volume()
    await bot.send(event, ret, at_sender=False)


@stock.handle()
async def stock(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext()
    if 'sh' in msg:
        ret = await data_source.get_stock(stock_code=msg)
    else:
        ret = await data_source.get_stock(stock_name=msg)
    await bot.send(event, str(ret), at_sender=False)


''' >>>>>> EXP Function for Utils <<<<<< '''


@exp_cryptocoin.handle()
async def _exp_cryptocoin(bot: Bot, event: MessageEvent):
    instrument_id = event.get_plaintext().upper()
    ret = data_source.coin_exp_get_price(instrument_id)
    await bot.send(event, ret, at_sender=False)


'''
@driver.on_bot_connect
async def do_something(bot: Bot):
    group_id = ***
    msg = 'Jarvis now already back online, Sir'
    await bot.send_group_msg(group_id=group_id, message=msg, auto_escape=True)
'''


async def cron_daily_coin():
    ret = await data_source.get_coin_volume()
    await _scheduler_controller(ret)


async def cron_daily_news():
    ret_1 = data_source.rss_get_news('药闻')
    await _scheduler_controller(ret_1)


async def cron_currency():
    ret = _currency()
    await _currency_scheduler_controller(ret)


async def cron_daily_stock():
    holiday = is_public_holiday()
    if isinstance(holiday, Holiday):
        await _scheduler_controller('今天是 %s，A股休市' % holiday.name)
        return

    if holiday in (6, 7):
        today = '星期六' if holiday == 6 else '星期天'
        await _scheduler_controller('今天是 %s，A股休市' % today)
        return

    now = datetime.datetime.now()
    today = '%d年%d月%d日' % (now.year, now.month, now.day)
    msg = await data_source.get_stock(stock_code='sh.000001')
    ret = '今天是' + today + '\n' + msg
    await _scheduler_controller(ret)


async def corn_daily_weather():
    gugu_door_cities = ['广州', '珠海', '东莞', '佛山', ]
    researcher_cities = ['广州', '北京', '深圳', '上海', '乌海', '梅州', '吉林', '杭州', '长春', ]

    bot = nonebot.get_bots().get('***')

    for city in gugu_door_cities:
        target = city + '天气'
        ret = data_source.weather_get(target)
        await bot.send_group_msg(group_id=***, message=ret, auto_escape=True)
        if gugu_door_cities.index(city) != len(gugu_door_cities) - 1:
            await asyncio.sleep(30)

    for city in researcher_cities:
        target = city + '天气'
        ret = data_source.weather_get(target)
        await bot.send_group_msg(group_id=***, message=ret, auto_escape=True)
        if researcher_cities.index(city) != len(researcher_cities) - 1:
            await asyncio.sleep(30)


async def _scheduler_controller(message: str):
    groups = [***, ***]
    bot = nonebot.get_bots()['***']
    for group_id in groups:
        await bot.send_group_msg(group_id=group_id, message=message, auto_escape=True)
        await asyncio.sleep(random.choice([i for i in range(30, 60)]))


async def _currency_scheduler_controller(message: str):
    groups = [***, ***]
    bot = nonebot.get_bots()['***']
    for group_id in groups:
        await bot.send_group_msg(group_id=group_id, message=message, auto_escape=True)
        await asyncio.sleep(random.choice([i for i in range(30, 60)]))


def _currency():
    rate_results = get_rate()

    # 美元
    usd_to_cny = round(1/rate_results.get('USD'), 5)
    # 英镑
    gbp_to_cny = round(1/rate_results.get('GBP'), 3)
    # 欧元
    eur_to_cny = round(1/rate_results.get('EUR'), 3)
    # 澳大利亚元
    aud_to_cny = round(1/rate_results.get('AUD'), 3)
    # 瑞士法郎
    chf_to_cny = round(1/rate_results.get('CHF'), 3)
    # 港元
    hkd_to_cny = round(1/rate_results.get('HKD'), 3)
    # 日元
    cny_to_jpy = round(rate_results.get('JPY'), 3)
    # 俄罗斯卢布
    rub_to_cny = round(rate_results.get('RUB'), 3)
    # 乌克兰格里夫纳
    cny_to_uah = round(rate_results.get('UAH'), 3)

    cny_to_cnh = round(rate_results.get('CNH'), 3)

    ret = '💰 在岸人民币汇率 💰\n\n¥ 1 (CNY) = ¥ ' + f'{cny_to_cnh}' + ' (CNH)\n\n1 美元 ≈ ¥ ' + f'{usd_to_cny}' +\
          '\n1 英镑 ≈ ¥ ' + f'{gbp_to_cny}' + '\n1 欧元 ' + '≈ ¥ ' + f'{eur_to_cny}' + '\n1 澳大利亚元 ≈ ¥ ' +\
          f'{aud_to_cny}' + '\n1 瑞士法郎 ≈ ¥ ' + f'{chf_to_cny}' + '\n1 港元 ≈ ¥ ' + f'{hkd_to_cny}' +\
          '\n1 日元 ≈ ¥ ' + f'{cny_to_jpy}' + '\n\n¥ 1 ≈ ' + f'{rub_to_cny}' + ' 俄罗斯卢布\n¥ 1 ≈ ' + f'{cny_to_uah}' +\
          ' 乌克兰格里夫纳 '

    return ret


scheduler.add_job(cron_daily_news, "cron", hour=8, minute=2, id="news")
scheduler.add_job(cron_daily_coin, "cron", hour=7, minute=32, id="coins")
scheduler.add_job(corn_daily_weather, 'cron', hour=8, minute=32, id='weather')
scheduler.add_job(cron_daily_stock, 'cron', hour=15, minute=17, id='stock')

# currency
scheduler.add_job(cron_currency, 'cron', hour=0, minute=1, id='currency1')
scheduler.add_job(cron_currency, 'cron', hour=10, minute=1, id='currency2')
scheduler.add_job(cron_currency, 'cron', hour=15, minute=1, id='currency3')
scheduler.add_job(cron_currency, 'cron', hour=21, minute=1, id='currency4')
