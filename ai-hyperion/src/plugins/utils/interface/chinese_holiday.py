import datetime
import time
from typing import Union, Type

import requests


class Holiday:
    def __init__(self, name: str, date: str, is_off_day: str):
        self.name: str = name
        self.date = date
        self.is_off_day: bool = True if is_off_day == 'true' else False

    def __str__(self):
        return '节日名称: %s, \n日期: %s, \n放假: %s' \
               % (self.name, self.date, "放假" if self.is_off_day else "不放假")


def get_chinese_holidays() -> list[Holiday]:
    now = datetime.datetime.now()
    current_year = now.year.__str__()

    url = 'https://natescarlet.coding.net/p/github/d/holiday-cn/git/raw/master/' + current_year + '.json'

    res = requests.get(url)
    days = res.json().get('days')
    holidays = []

    for day in days:
        holidays.append(
            Holiday(
                day.get('name'),
                day.get('date'),
                day.get('isOffDay')
            ))

    return holidays


def is_public_holiday() -> Union[int, Holiday]:
    holidays = get_chinese_holidays()
    now = datetime.datetime.now()

    current_date = time.strftime('%Y-%m-%d', now.timetuple())
    for _ in holidays:
        if current_date == _.date:
            return _

    if now.isoweekday() in (6, 7):
        return now.isoweekday()


if __name__ == '__main__':
    holiday = is_public_holiday()
    print(holiday)
