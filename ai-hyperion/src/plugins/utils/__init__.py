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

queshi = on_regex('(确实|qs|有一说一|yysy)')
traffic = on_regex('^(查流量|魔法|Magic|magic)$')
bitcoin = on_regex('^(BTC|btc|比特币|来点BTC|来点btc|来丶BTC|来丶btc)$')

@queshi.handle()
async def _queshi(bot: Bot, event: MessageEvent):
    text = "确实"
    await bot.send(event, text, at_sender=False)


@traffic.handle()
async def _traffic(bot: Bot, event: MessageEvent):
    dicts = data_source.magic_get_usage()
    result = data_source.magic_construct_string(dicts)
    await bot.send(event, result, at_sender=False)


@bitcoin.handle()
async def _bitcoin(bot: Bot, event: MessageEvent):
    dicts = data_source.btc_get_price()
    result = data_source.btc_construct_string(dicts)
    await bot.send(event, result, at_sender=False)
