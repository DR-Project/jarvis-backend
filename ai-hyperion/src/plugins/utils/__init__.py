import nonebot

from .config import Config
from nonebot import get_driver, require
from nonebot.plugin import on_regex, on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

import re

from . import data_source

global_config = get_driver().config
config = Config(**global_config.dict())
driver = nonebot.get_driver()
scheduler = require('nonebot_plugin_apscheduler').scheduler

# Constant List

REG_TRAFFIC = '^(查流量|魔法|Magic|CXLL)$'
REG_COIN = '^(BTC|EOS|BTG|ADA|DOGE|LTC|ETH|' + \
            'BCH|BSV|DOT|ATOM|UNI|ZEC|SUSHI|DASH|OKB|OKT|' + \
            'BTT|FLOW|AE|SHIB|BCD|NANO|WAVES|XCH|TRX|JWT|WIN)$'
REG_HOTCOIN = '(热门货币|hotcoin)'
REG_NEWS = '^(药闻|热搜|TESTNEWS)$'
REG_WEATHER = '^.*(天气)$'
REG_DDL = '^(DDL)$'
EREG_COIN = 'ECOIN'
REG_COVID_VACC = 'COVID'

# Register Event

traffic = on_regex(REG_TRAFFIC, re.IGNORECASE)
cryptocoin = on_regex(REG_COIN, re.IGNORECASE)
hotcoin = on_regex(REG_HOTCOIN)
mars_news = on_regex(REG_NEWS)
weather = on_regex(REG_WEATHER)
ass_ddl = on_regex(REG_DDL, re.IGNORECASE)
exp_cryptocoin = on_command(EREG_COIN)
covid_vacc = on_regex(REG_COVID_VACC, re.IGNORECASE)


''' >>>>>> Core Function for Utils <<<<<< '''


@traffic.handle()
async def _traffic(bot: Bot, event: MessageEvent):
    ret = data_source.magic_get_usage()
    await bot.send(event, ret, at_sender=False)


@cryptocoin.handle()
async def _cryptocoin(bot: Bot, event: MessageEvent):
    coin_type = event.get_plaintext().upper()
    ret = data_source.coin_get_price(coin_type)
    await bot.send(event, ret, at_sender=False)


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
    ret = data_source.ddl_get()
    await bot.send(event, ret, at_sender=False)


@covid_vacc.handle()
async def _covid_vacc(bot: Bot, event: MessageEvent):
    ret = await data_source.covid_get_vaccinations()
    await bot.send(event, ret, at_sender=False)


@hotcoin.handle()
async def hotcoin(bot: Bot, event: MessageEvent):
    ret = await data_source.get_coin_volume()
    await bot.send(event, ret, at_sender=False)


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


async def cron_daily_covid():
    ret = await data_source.covid_get_vaccinations()
    await _scheduler_controller(ret)


async def _scheduler_controller(message: str):
    groups = [***, ***]
    bot = nonebot.get_bots()['***']
    for group_id in groups:
        await bot.send_group_msg(group_id=group_id, message=message, auto_escape=True)


scheduler.add_job(cron_daily_news, "cron", hour=8, id="news")
scheduler.add_job(cron_daily_coin, "cron", hour=7, minute=30, id="coins")
scheduler.add_job(cron_daily_covid, "cron", hour=7, id="covid")
