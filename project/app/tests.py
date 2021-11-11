from data import get_data_from_weather_api


def test_response_get_data_from_weather_api():
    """Тест 1. Проверяет ответ от сервера """
    assert get_data_from_weather_api(mode="test") == 200, "Should be 200"


def test_type_get_data_from_weather_api():
    """"""
    assert type(
        get_data_from_weather_api()) == dict, "Should be a dictionary"


def test_content_response_get_data_from_weather_api():
    """"""
    assert get_data_from_weather_api()[
        "openweathermap"] != {}, "Openweathermap should not be empty"

    assert get_data_from_weather_api()[
        "weatherbit"] != {}, "Weatherbit should not be empty"


test_list = [test_response_get_data_from_weather_api,
             test_type_get_data_from_weather_api,
             test_content_response_get_data_from_weather_api,
             ]


if __name__ == "__main__":
    for index, test in enumerate(test_list):
        test()
        print(f"Test {index + 1} passed.")
    print("*******All tests passed*******")
