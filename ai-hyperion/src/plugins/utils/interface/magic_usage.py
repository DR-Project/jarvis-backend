import httpx
import json


def get_usage() -> dict:
    """

    :return: the key message to upstream
    """

    url = 'https://api.64clouds.com/v1/getServiceInfo?'

    param = {
        'veid': '***',
        'api_key': '***'
    }
    try:
        r = httpx.get(url, params=param)
        # print(r.url)
        payload = r.json()
    except httpx.RequestError:
        raise Exception('Interface Error / 接口错误')
    else:

        # print(json.dumps(payload))

        # "data_next_reset" "data_counter" "plan_monthly_data" "suspended"

        msg = {
            'data_next_reset': payload['data_next_reset'],
            'data_counter': payload['data_counter'],
            'plan_monthly_data': payload['plan_monthly_data'],
            'suspended': payload['suspended']
        }

    # print(json.dumps(msg))
    return msg


def construct_string(msg: dict) -> str:
    """

    :param msg: msg is a dict from upstream method
    :return: the message that will forward to QQ
    """

    # init variable
    data_usage = (msg['data_counter'] / 1024 / 1024 / 1024)
    data_usage = round(data_usage, 2)
    plan_monthly_data = (msg['plan_monthly_data'] / 1024 / 1024 / 1024)
    plan_monthly_data = round(plan_monthly_data, 2)

    # TODO
    suspended = msg['suspended']
    data_next_reset = msg['data_next_reset']

    left_data = plan_monthly_data - data_usage
    left_data = round(left_data, 2)
    ret = '本月魔法剩余' + f'{left_data}' + ' GB, 已经使用 ' + f'{data_usage}' + ' GB.'

    return ret
