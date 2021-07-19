import datetime
from typing import List, Dict, Any, Optional

import baostock as bs
import pandas as pd


class QueryOccurException(Exception):
    pass


def get_stock_price(stock_name: str = None, stock_code: str = None):
    if stock_code or stock_name:
        bs.login()

        if stock_name:
            rs = bs.query_stock_basic(code_name=stock_name)
            if rs.error_code == '0' and len(rs.data) >= 1:
                return rs.data[0][0]
            else:
                raise QueryOccurException('查询股票代码出现错误')
        else:
            bs.logout()
            return stock_code


def get_k_data(stock_code: str):

    now_date = datetime.date.today()

    date_before_seven_days = _get_7_days_before()

    bs.login()

    rs = bs.query_history_k_data_plus("sh.600000",
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,"
                                      "tradestatus,pctChg,isST",
                                      start_date=date_before_seven_days.__str__(), end_date=now_date.__str__(),
                                      frequency="d", adjustflag="3")

    return rs.data


def _get_7_days_before():

    now_date = datetime.date.today()

    seven_days = datetime.timedelta(days=7)

    date_before_seven_days = now_date - seven_days

    return date_before_seven_days


def draw_k_line_chart(k_data: list):
    pass


if __name__ == '__main__':
    print(get_k_data('sh.600519'))
