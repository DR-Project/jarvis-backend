from typing import List, Dict, Any
import httpx


def get_usage() -> List[Dict[str, Any]]:
    """

    :return: a list contain all the server usage data
    """

    param_1 = {
        'veid': '***',
        'api_key': '***'
    }

    param_2 = {
        'veid': '***',
        'api_key': '***'
    }

    magic_info = {
        'fork-02': 'Himeko',
        'fork-01': 'Carrier'
    }

    params = [param_1, param_2]
    ret = []
    try:
        for param in params:
            data = ''
            for k, v in param.items():
                data += k + '=' + v + '&'

            url = 'https://api.64clouds.com/v1/getServiceInfo?' + data

            r = httpx.get(url)
            payload = r.json()

            msg = {
                'data_next_reset': payload['data_next_reset'],
                'data_counter': payload['data_counter'],
                'plan_monthly_data': payload['plan_monthly_data'],
                'suspended': payload['suspended'],
                'node_name': magic_info[payload['hostname']]
            }

            ret.append(msg)

    except httpx.RequestError:
        raise Exception('Interface Error / 接口错误')
    return ret


if __name__ == '__main__':
    print(get_usage())
