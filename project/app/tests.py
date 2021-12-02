from data import get_data_from_weather_api
import requests
import itertools
import threading
import time
import sys


def loading(function):
    def wrapper():
        done = False

        def animate():
            """Animated ASCII loading in termminal"""
            SPEED = 1  # Int 1 - 10
            LINE = '\rLoading '

            frames = [
                ["⡏ ", "⡗ ", "⡧ ", "⣇ ", "⣸ ", "⢼ ", "⢺ ", "⢹ "],
                ['bq', 'dp', 'qb', 'pd'],
                ['bo', 'do', 'ob', 'od', 'oq', 'op', 'qo', 'po'],
                ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"],
            ]

            for frame in itertools.cycle(frames[0]):

                if done:
                    break
                sys.stdout.write(LINE + frame)
                sys.stdout.flush()
                time.sleep(1 / SPEED / 10)
            sys.stdout.write('\rDone!' + ' ' * (len(LINE) + 2))

        thread = threading.Thread(target=animate)
        thread.start()

        function()

        done = True
    return wrapper


def test_response_get_data_from_weather_api():
    """Тест 1. Проверяет ответ от сервера погоды"""
    assert get_data_from_weather_api(mode="test") == 200, "Should be 200"


def test_type_get_data_from_weather_api():
    """Тест 2. Проверяет является ли словарём результат работы функции"""
    assert type(
        get_data_from_weather_api()) == dict, "Should be a dictionary"


def test_content_response_get_data_from_weather_api():
    """Тест 3. Проверяет не ялвются ли ответы от погодных
    сервисов пустыми словарями"""
    assert get_data_from_weather_api()[
        "openweathermap"] != {}, "Openweathermap should not be empty"

    assert get_data_from_weather_api()[
        "weatherbit"] != {}, "Weatherbit should not be empty"


def test_ping_response():
    """Тест 4. При включенном сервере, проверяет его работу"""
    assert requests.get(
        "http://localhost:8000/ping").content.decode() == '{"ping":"pong!"}'


test_list = [test_response_get_data_from_weather_api,
             test_type_get_data_from_weather_api,
             test_content_response_get_data_from_weather_api,
             test_ping_response,
             ]


@loading
def auto_tester():
    if __name__ == "__main__":
        for index, test in enumerate(test_list):
            test()
            print("\r                  ", end='')
            print(f"\rTest {index + 1} passed.")
        print("*******All tests passed*******")


auto_tester()
