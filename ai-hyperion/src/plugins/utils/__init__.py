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

REG_TRAFFIC     = '^(查流量|魔法|Magic|magic|cxll)$'
REG_COIN        = '^(BTC|btc|EOS|eos|BTG|btg|ADA|ada|DOGE|doge|LTC|ltc|ETH|eth)$'

# Register Event

traffic         = on_regex(REG_TRAFFIC)
cryptocoin      = on_regex(REG_COIN)


''' >>>>>> Core Function for Utils <<<<<< '''


@traffic.handle()
async def _traffic(bot: Bot, event: MessageEvent):
    dicts = data_source.magic_get_usage()
    result = data_source.magic_construct_string(dicts)
    await bot.send(event, result, at_sender=False)


@cryptocoin.handle()
async def _cryptocoin(bot: Bot, event: MessageEvent):
    coin_type = event.get_plaintext().upper()
    try:
        dicts = data_source.coin_get_price(data_source.cryptocurrency[coin_type])
        result = data_source.coin_construct_string(dicts)
    except: 
        result = "接口异常"
        await bot.send(event, result, at_sender=False)
    else:
        await bot.send(event, result, at_sender=False)
