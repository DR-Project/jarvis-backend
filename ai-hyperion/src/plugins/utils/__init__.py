from .config import Config

from nonebot import get_driver
from nonebot.plugin import on_regex, on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

import re

from . import data_source

global_config = get_driver().config
config = Config(**global_config.dict())

# Constant List

REG_TRAFFIC = '^(查流量|魔法|Magic|magic|cxll|CXLL)$'
REG_COIN = '^(BTC|EOS|BTG|ADA|DOGE|LTC|ETH|' + \
           'BCH|BSV|DOT|ATOM|UNI|ZEC|SUSHI|DASH|OKB|OKT)$'
REG_NEWS = '^(药闻|热搜|TESTNEWS)$'
REG_WEATHER = '^.*(天气)$'
REG_DDL = '^(DDL|ddl)$'
EREG_COIN = 'ECOIN'
COVID_VACC = 'COVID'

# Register Event

traffic = on_regex(REG_TRAFFIC)
cryptocoin = on_regex(REG_COIN, re.IGNORECASE)
mars_news = on_regex(REG_NEWS)
weather = on_regex(REG_WEATHER)
ass_ddl = on_regex(REG_DDL)
exp_cryptocoin = on_command(EREG_COIN)
covid_vacc = on_regex(COVID_VACC)

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


''' >>>>>> EXP Function for Utils <<<<<< '''


@exp_cryptocoin.handle()
async def _exp_cryptocoin(bot: Bot, event: MessageEvent):
    instrument_id = event.get_plaintext().upper()
    ret = data_source.coin_exp_get_price(instrument_id)
    await bot.send(event, ret, at_sender=False)

# 你下次测试一下这段代码，这块我不熟
'''driver = get_driver()


@driver.on_startup
async def do_something():

    bot = Bot(driver, 'websocket', config, '***')
    group_id = ***
    msg = 'Jarvis already back online, Sir.'
    await bot.send_group_msg(group_id=group_id, message=msg, auto_escape=True)'''
