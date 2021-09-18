#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2020-09-18 00:15:21
@LastEditors    : yanyongyu
@LastEditTime   : 2021-03-16 16:59:22
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

import datetime
import time, psutil

from typing import List, Dict


def cpu_status() -> float:
    return psutil.cpu_percent(interval=1)  # type: ignore


def per_cpu_status() -> List[float]:
    return psutil.cpu_percent(interval=1, percpu=True)  # type: ignore


def memory_status() -> float:
    return psutil.virtual_memory().percent


def disk_usage() -> Dict[str, psutil._common.sdiskusage]:
    disk_parts = psutil.disk_partitions()
    disk_usages = {
        d.mountpoint: psutil.disk_usage(d.mountpoint) for d in disk_parts
    }
    return disk_usages


def uptime() -> str:
    time_seconds = int(time.time() - psutil.boot_time())
    return time_format(time_seconds, preset='en')


def time_format(timestamp: int, preset='std') -> str:
    """
    格式化输出剩余时间信息。

    参数：
    - `timestamp: int`：时间戳。

    关键字参数：
    - `preset: str`：格式名称，可用的格式名称有：
        - `std`：标准格式，以冒号分隔日、时、分、秒，例如 `05:04:03:02`；
        - `zh`：中文格式，例如 `5天4小时3分2秒`。
      默认值为 `std`。

    返回：
    - `str`：格式化的时间信息

    代码来源：
    https://github.com/jks15satoshi/nonebot_plugin_cooldown
    """
    days = abs(timestamp) // 86400
    hours = (abs(timestamp) - days * 86400) // 3600
    minutes = (abs(timestamp) - days * 86400 - hours * 3600) // 60
    seconds = abs(timestamp) - days * 86400 - hours * 3600 - minutes * 60

    if preset == 'std':
        return (f'{str(days).zfill(2)}:{str(hours).zfill(2)}:'
                f'{str(minutes).zfill(2)}:{str(seconds).zfill(2)}')

    if preset == 'zh':
        result = []
        if days:
            result.append(f'{days}天')
        if hours:
            result.append(f'{hours}小时')
        if minutes:
            result.append(f'{minutes}分')
        if seconds or (not days and not hours and not minutes):
            result.append(f'{seconds}秒')

            return ''.join(result)

    if preset == 'en':
        return str(datetime.timedelta(seconds=timestamp))


if __name__ == "__main__":
    print(cpu_status())
    print(memory_status())
    print(disk_usage())
    print(uptime())
