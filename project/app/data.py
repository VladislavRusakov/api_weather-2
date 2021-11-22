import requests
import os
from typing import Dict
import dotenv
import json
import datetime

dotenv.load_dotenv('.env')
API_KEY = os.environ['OPENWEATHERMAP_API_KEY']
API_KEY2 = os.environ['WEATHERBIT_API_KEY']


def get_data_from_weather_api(
        city: str = "moscow",
        appid1: str = API_KEY,
        appid2: str = API_KEY2,
        mode: str = "normal") -> Dict[str, Dict[str, str]]:
    """Получает данные с API сайтов, формирует словарь с ключами
        name, timezone, lon, lat, temperature и source"""
    url = "https://api.openweathermap.org/data/2.5/weather"

    response = requests.get(url, params={
        "q": city,
        "appid": appid1,
        "units": "metric",
        })

    if mode != "normal":
        return response.status_code

    data = {'openweathermap': {
            'name': response.json()['name'],
            'timezone': response.json()['timezone'],
            'lon': response.json()['coord']['lon'],
            'lat': response.json()['coord']['lat'],
            'temperature': response.json()['main']['temp'],
            'source': url
            }}

    url = 'https://api.weatherbit.io/v2.0/current'

    response = requests.get(url, params={
        'city': city,
        "key": appid2,
    })

    data["weatherbit"] = {
        'name': response.json()['data'][0]['city_name'],
        'timezone': response.json()['data'][0]['timezone'],
        'lon': response.json()['data'][0]['lon'],
        'lat': response.json()['data'][0]['lat'],
        'temperature': response.json()['data'][0]['temp'],
        'source': url
    }

    return data


def post_request_sender(data: dict) -> dict:
    """"""
    req1 = {}
    req2 = {}
    time = datetime.datetime.now().strftime("%Y-%m-%d.%H:%M")

    src = data["openweathermap"]
    req1 = {"source": "openweathermap",
            "city": src["name"],
            "temp": src["temperature"],
            "timezone": src["timezone"],
            "lon": src["lon"],
            "lat": src["lat"],
            "request": "http://localhost:8000/api/" + src["name"],
            "datetime": time
            }

    src = data["weatherbit"]
    req2 = {"source": "weatherbit",
            "city": src["name"],
            "temp": src["temperature"],
            "timezone": src["timezone"],
            "lon": src["lon"],
            "lat": src["lat"],
            "request": "http://localhost:8000/api/" + src["name"],
            "datetime": time
            }

    requests.post('http://localhost:8000/db', data=json.dumps(req1))
    requests.post('http://localhost:8000/db', data=json.dumps(req2))
