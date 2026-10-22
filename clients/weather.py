from clients.http import (
    NotFoundError,
    ServiceUnavailableError,
    get_json,
)


WEATHER_CODES = {
    0: "ясно",
    1: "преимущественно ясно",
    2: "переменная облачность",
    3: "пасмурно",
    45: "туман",
    48: "туман",
    51: "морось",
    53: "морось",
    55: "сильная морось",
    61: "дождь",
    63: "дождь",
    65: "сильный дождь",
    71: "снег",
    73: "снег",
    75: "сильный снег",
    80: "ливень",
    81: "ливень",
    82: "сильный ливень",
    95: "гроза",
    96: "гроза с градом",
    99: "гроза с градом",
}


def get_weather(city: str) -> dict:
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_data = get_json(
        geo_url,
        params={"name": city, "count": 1, "language": "en"},
    )

    results = geo_data.get("results")

    if not isinstance(results, list) or not results:
        raise NotFoundError(f"Город '{city}' не найден")

    location = results[0]

    if not isinstance(location, dict):
        raise ServiceUnavailableError("Некорректные данные геокодирования")

    latitude = location.get("latitude")
    longitude = location.get("longitude")

    if not all(
        isinstance(value, (int, float)) and not isinstance(value, bool)
        for value in (latitude, longitude)
    ):
        raise ServiceUnavailableError("Координаты города отсутствуют")

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_data = get_json(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code",
        },
    )

    current = weather_data.get("current")

    if not isinstance(current, dict):
        raise ServiceUnavailableError("Данные о погоде отсутствуют")

    temperature = current.get("temperature_2m")
    code = current.get("weather_code")

    if (
        not isinstance(temperature, (int, float))
        or isinstance(temperature, bool)
        or not isinstance(code, int)
        or isinstance(code, bool)
    ):
        raise ServiceUnavailableError("Некорректные данные о погоде")

    return {
        "city": location.get("name", city),
        "temp_c": float(temperature),
        "description": WEATHER_CODES.get(code, "неизвестная погода"),
    }