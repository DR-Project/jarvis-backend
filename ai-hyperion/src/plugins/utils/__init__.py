# import nonebot
from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass


from nonebot.plugin import on_regex, on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot import require

from . import data_source

import re

# Load crontab plugin
# scheduler = require('nonebot_plugin_apscheduler').scheduler


# Constant List

REG_TRAFFIC = '^(查流量|魔法|Magic|magic|cxll|CXLL)$'
REG_COIN = '^(BTC|EOS|BTG|ADA|DOGE|LTC|ETH|' + \
            'BCH|BSV|DOT|ATOM|UNI|ZEC|SUSHI|DASH|OKB|OKT)$'
REG_NEWS = '^(药闻|热搜|TESTNEWS)$'
REG_WEATHER = '^.*(天气)$'
REG_DDL = '^(DDL|ddl)$'
EREG_COIN = 'ECOIN'


# Register Event

traffic = on_regex(REG_TRAFFIC)
cryptocoin = on_regex(REG_COIN, re.IGNORECASE)
mars_news = on_regex(REG_NEWS)
weather = on_regex(REG_WEATHER)
ass_ddl = on_regex(REG_DDL)
exp_cryptocoin = on_command(EREG_COIN)


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


''' >>>>>> EXP Function for Utils <<<<<< '''


@exp_cryptocoin.handle()
async def _exp_cryptocoin(bot: Bot, event: MessageEvent):
    instrument_id = event.get_plaintext().upper()
    ret = data_source.coin_exp_get_price(instrument_id)
    await bot.send(event, ret, at_sender=False)
