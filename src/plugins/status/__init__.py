#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2020-09-18 00:00:13
@LastEditors    : yanyongyu
@LastEditTime   : 2021-03-16 17:05:58
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"


from nonebot import get_driver, on_command, on_notice
from nonebot.adapters.cqhttp import PokeNotifyEvent, Bot, MessageEvent
from nonebot.typing import T_State

from .config import Config
from .data_source import cpu_status, per_cpu_status, memory_status, disk_usage, uptime
from ..settings.manager import is_permission_valid

global_config = get_driver().config
status_config = Config(**global_config.dict())

command = on_command('status')
group_poke = on_notice()


@command.handle()
async def server_status(bot: Bot, event: MessageEvent):
    lsp = event.get_user_id()
    data = send_status(lsp)
    await bot.send(event, '\n'.join(data), at_sender=False)


def send_status(user_id: str) -> list:
    if is_permission_valid(user_id):
        data = []

        if status_config.server_status_cpu:
            if status_config.server_status_per_cpu:
                data.append("CPU:")
                for index, per_cpu in enumerate(per_cpu_status()):
                    data.append(f"  core{index + 1}: {int(per_cpu):02d}%")
            else:
                data.append(f"CPU: {int(cpu_status()):02d}%")

        if status_config.server_status_memory:
            data.append(f"Memory: {int(memory_status()):02d}%")

        if status_config.server_status_disk:
            data.append("Disk:")
            for k, v in disk_usage().items():
                data.append(f"  {k}: {int(v.percent):02d}%")
        
        if status_config.server_status_uptime:
            data.append(f"Uptime: {uptime()}")

        return data
    return ['Permission Denied. Please contact administrator. ']


@group_poke.handle()
async def _group_poke(bot: Bot, event: PokeNotifyEvent, state: T_State) -> bool:
    lsp = event.get_user_id()
    print(event.is_tome)
    if isinstance(event, PokeNotifyEvent) and event.is_tome():
        data = send_status(lsp)
        await bot.send(event, '\n'.join(data), at_sender=False)
