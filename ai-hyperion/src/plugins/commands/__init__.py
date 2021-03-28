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

# Constant List

REG_HELP        = '^(Jarvis|贾维斯|命令列表)$'

# Register Event

help_list       = on_regex(REG_HELP)


''' >>>>>> Core Function for Commands <<<<<< '''


@help_list.handle()
async def _help_list(bot: Bot, event: MessageEvent):
    lists = [{
        'type': 'text',
        'data': {
            'text': " __Command List v0.1__ \n"
        }
    },{
        'type': 'text',
        'data': {
            'text': " [Magic/魔法] \n> 查询Magic流量 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': " [BTG/LTC/...] \n> 数字货币价格 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': " [丢人/diu] \n> 随机抽取幸运儿 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': " [色来/selai] \n> 在鹿上了 0% \n",
        }
    }]
    await bot.send(event, lists, at_sender=False)