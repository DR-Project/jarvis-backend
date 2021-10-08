import csv
import httpx


class NoDefineException(Exception):
    """
    defined a NoDefineException
    """


class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def get_coordinate(self):
        return self.lat, self.lng


def _get_weather(location: Location, hourly_steps=24) -> dict:
    lat, lng = location.get_coordinate()

    url = 'https://api.caiyunapp.com/v2.5/%s/%s,%s/hourly.json?hourlysteps=%s' % (caiyun_apikey, lng, lat, hourly_steps)

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
    # todo: you can move this method to __init__.py replace original(old) one
    weather_data = _get_weather(location, hourly_steps)

    temperature_max, temperature_min = weather_data.get('temperature_max'), weather_data.get('temperature_min')

    ret = [
        weather_data.get('forecast_keypoint'),
        '气温 %s到%s°C，' % (temperature_min, temperature_max),
        '空气质量%s。' % weather_data.get('max_air_quality')
    ]

    print(''.join(ret))
    return ret


def get_location(address: str) -> Location:
    file = 'C:\\Users\\ljd69\\PycharmProjects\\Ai-Hyperion\\src\\plugins\\utils\\data\\china_cities.csv'
    # todo: fix file path

    with open(file, encoding='utf-8') as csv_file:
        _ = csv.DictReader(csv_file)
        china_cities_coordinate = []

        for row in _:
            china_cities_coordinate.append(row)

        tmp = [x for x in china_cities_coordinate if address in x.get('district')]
        if not tmp:
            for i in china_cities_coordinate:
                if address in i.get('city'):
                    tmp = i
                    break

        if isinstance(tmp, list):
            tmp = tmp[0]

        lat, lng = tmp.get('lat'), tmp.get('lng')
        return Location(lat, lng)


def _get_file() -> str:
    # todo: fix file path
    import os
    file = os.getcwd() + '/src/plugins/utils/data/' + 'china_cities.csv'
    return file


if __name__ == '__main__':
    coordinate = get_location('广州')
    print(_get_weather(coordinate))
