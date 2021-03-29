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


from nonebot.plugin import on_regex
from nonebot.adapters.cqhttp import Bot, MessageEvent

from . import data_source

# Constant List

REG_TRAFFIC = '^(查流量|魔法|Magic|magic|cxll|CXLL)$'
REG_COIN = '^(BTC|btc|EOS|eos|BTG|btg|ADA|ada|DOGE|doge|LTC|ltc|ETH|eth)$'
REG_NEWS = '^(药闻)$'

# Register Event

traffic = on_regex(REG_TRAFFIC)
cryptocoin = on_regex(REG_COIN)
mars_news = on_regex(REG_NEWS)


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
    ret = data_source.mars_get_news()
    await bot.send(event, ret, at_sender=False)