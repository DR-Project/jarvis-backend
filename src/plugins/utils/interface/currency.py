import httpx


def get_rate() -> dict:
    url = 'https://api.fastforex.io/fetch-all?from=CNY&api_key=demo'

    try:
        r = httpx.get(url)
    except httpx.RequestError:
        raise Exception('Interface Error / 接口异常')
    else:
        msg = r.json()

        return msg.get('results')
