from .config import Config

from nonebot import get_driver
from nonebot.plugin import on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

from . import data_source
from ..settings.manager import is_permission_valid


global_config = get_driver().config
config = Config(**global_config.dict())


# Constant List

REG_COLORFUL = '^(色来)$|^(来点|来丶)(色图|涩图|嗷图)$|^(色图|涩图|嗷图)$|^(给点给点)$'
REG_COLORFLAG = '^涩图(ON|OFF)$'


# Register Event

colorful = on_regex(REG_COLORFUL)
color_flag = on_regex(REG_COLORFLAG)


''' >>>>>> Core Function for Colorful <<<<<< '''


@colorful.handle()
async def _colorful(bot: Bot, event: MessageEvent):
    lsp = event.user_id

    if is_permission_valid(lsp):
        ret = await data_source.get_colorful(lsp)
    else:
        if data_source.SWITCH_FLAG:
            ret = await data_source.get_colorful(lsp)
        else:
            ret = data_source.get_crepper(lsp)
    await bot.send(event, ret, at_sender=False)


@color_flag.handle()
async def _color_flag(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext()
    lsp = event.user_id
    if is_permission_valid(lsp):
        if msg == '涩图ON':
            data_source.SWITCH_FLAG = True
            ret = 'GKD'
            await bot.send(event, ret, at_sender=False)
        else:
            data_source.SWITCH_FLAG = False
    else:
        if msg == '涩图ON':
            ret = '不许色！'
            await bot.send(event, ret, at_sender=False)
        else:
            pass
