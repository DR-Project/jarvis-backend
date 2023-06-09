#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBot_V11_Adapter

# Custom your logger
# 
from nonebot.log import logger, default_format
logger.add(
        "./logs/latest.log",
        level='INFO',
        enqueue=True,
        rotation="00:00",
        compression='zip',
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
        colorize=False,
    )

# You can pass some keyword args config to init function
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})

driver = nonebot.get_driver()
driver.register_adapter(OneBot_V11_Adapter)

nonebot.load_builtin_plugins()
# nonebot.load_from_toml("pyproject.toml")

# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...

# Discard by author, on longer used anymore
# Plugin testing for front-end
nonebot.load_plugin("src")
nonebot.load_plugin("nonebot_plugin_russian")

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
