import csv
import httpx
from nonebot import get_driver

from ..config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

DIR_WEATHER_CITIES = '/src/plugins/utils/data/'


class NoDefineException(Exception):
    """
    defined a NoDefineException
    """


class Location:
    def __init__(self, lat, lng, location_type=''):
        self.lat = lat
        self.lng = lng
        self.location_type = location_type

        if location_type in ('c', 'd'):
            self.location_type = '市' if location_type == 'c' else '区'

    def get_coordinate(self):
        return self.lat, self.lng

    def get_type(self):
        return self.location_type


def _get_weather(location: Location, hourly_steps=24) -> dict:
    lat, lng = location.get_coordinate()

    url = 'https://api.caiyunapp.com/v2.5/%s/%s,%s/hourly.json?hourlysteps=%s' % (config.caiyun_apikey, lng, lat,
                                                                                  hourly_steps)

    res = httpx.get(url)

    if not res.json().get('status') == 'ok':
        raise NoDefineException

    result = res.json().get('result')

    temperatures = [x.get('value') for x in result['hourly']['temperature']]
    air_qualities = [x.get('value').get('chn') for x in result['hourly']['air_quality']['aqi']]

    ret = {
        'forecast_keypoint': result.get('forecast_keypoint'),
        'temperature_max': '{:.0f}'.format(max(temperatures)),
        'temperature_min': '{:.0f}'.format(min(temperatures)),
        'max_air_quality': max(air_qualities)
    }

    return ret


def process_weather_data(location: Location, hourly_steps):

    weather_data = _get_weather(location, hourly_steps)

    temperature_max, temperature_min = weather_data.get('temperature_max'), weather_data.get('temperature_min')

    ret = [
        '%s，' % weather_data.get('forecast_keypoint'),
        '气温 %s到%s°C，' % (temperature_min, temperature_max),
        '空气质量%s。' % weather_data.get('max_air_quality')
    ]

    return ''.join(ret)


def get_location(address: str) -> [Location, None]:
    file = _get_file()

    with open(file, encoding='utf-8') as csv_file:
        _ = csv.DictReader(csv_file)
        china_cities_coordinate = []

        for row in _:
            china_cities_coordinate.append(row)

        tmp, location_type = [x for x in china_cities_coordinate if address in x.get('district')], 'd'
        if not tmp:
            for i in china_cities_coordinate:
                if address in i.get('city'):
                    tmp, location_type = i, 'c'
                    break

        if not tmp:
            return None

        if address in ('香港', '澳门'):
            location_type = ''

        if '台湾' in address:
            location_type = '省'

        if isinstance(tmp, list):
            tmp = tmp[0]

        lat, lng = tmp.get('lat'), tmp.get('lng')
        return Location(lat, lng, location_type)


def _get_file() -> str:
    import os
    file = os.getcwd() + DIR_WEATHER_CITIES + 'china_cities.csv'
    return file
