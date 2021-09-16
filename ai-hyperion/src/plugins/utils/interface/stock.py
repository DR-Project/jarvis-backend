import datetime
from typing import List, Dict, Any, Optional

import baostock as bs
import pandas as pd


class QueryOccurException(Exception):
    pass


class NoParamsException(Exception):
    pass


def _get_stock_code(stock_name: str = None, stock_code: str = None):
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


def _get_k_data(stock_code: str):

    now_date = datetime.date.today()

    date_before_seven_days = _get_7_days_before()

    bs.login()

    rs = bs.query_history_k_data_plus(stock_code,
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,"
                                      "tradestatus,pctChg,pbMRQ",
                                      start_date=date_before_seven_days.__str__(), end_date=now_date.__str__(),
                                      frequency="d", adjustflag="3")

    bs.logout()

    return rs.data


def _get_7_days_before():

    now_date = datetime.date.today()

    seven_days = datetime.timedelta(days=7)

    date_before_seven_days = now_date - seven_days

    return date_before_seven_days


def _get_latest_price(stock_code: str) -> list:
    """

    :param stock_code:
    :return: 返回一个列表。从0开始，按顺序为。0，日期；1，股票代码；2，开盘价；3，最高价；4，最低价；5，收盘价；6，前收盘价；7，成交量（累计，单位：股）；
    8，成交额（单位：人民币元）；9，复权状态(1：后复权， 2：前复权，3：不复权）；10，换手率；11，交易状态(1：正常交易 0：停牌）
    12，涨跌幅（百分比）；13，市净率；
    """
    return _get_k_data(stock_code)[-1]


def stock_controller(stock_name: str = None, stock_code: str = None):
    if stock_code or stock_name:

        if stock_code:
            return _get_latest_price(stock_code)
        else:
            code = _get_stock_code(stock_name=stock_name)
            return _get_latest_price(code)

    else:
        raise NoParamsException('至少需要传入一个参数')


def draw_k_line_chart(k_data: list):
    # todo
    pass


# if __name__ == '__main__':
#     print(get_latest_price('sh.000001'))
