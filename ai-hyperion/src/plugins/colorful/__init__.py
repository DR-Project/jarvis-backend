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
from nonebot.adapters.cqhttp import GroupMessageEvent

from . import data_source


# Constant List


REG_COLORFUL = '^(色来)$|^(来点|来丶)(色图|涩图)$|^(色图|涩图)|(给点给点)$'
REG_COLORFLAG = '^涩图(ON|OFF)$'

# Register Event

colorful = on_regex(REG_COLORFUL)
colorfalg = on_regex(REG_COLORFLAG)


''' >>>>>> Core Function for Colorful <<<<<< '''


@colorful.handle()
async def _colorful(bot: Bot, event: MessageEvent):
    lsp = event.get_user_id()
    if data_source.SWITCH_FLAG:
        ret = data_source.get_colorful()
    else:
        ret = data_source.get_crepper(lsp)
    await bot.send(event, ret, at_sender=False)


@colorfalg.handle()
async def _colorfalg(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext()
    lsp = event.get_user_id()
    if data_source.premission_valid(lsp):
        if msg == '涩图ON':
            data_source.SWITCH_FLAG = True
            ret = 'GKD'
        else:
            data_source.SWITCH_FLAG = False
            ret = '涩图OFF'
    else:
        if msg == '涩图ON':
            ret = '不许色！'
        else:
            ret = '摩多摩多！'
    await bot.send(event, ret, at_sender=False)
