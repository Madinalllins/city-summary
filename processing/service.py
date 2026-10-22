from clients.rates import get_rate
from clients.weather import get_weather
from processing.preprocessing import (
    is_expensive_rate,
    needs_warm_clothes,
)


def build_city_summary(
    city: str,
    currency: str = "USD",
) -> dict:
    weather = get_weather(city)
    rate = get_rate(currency)

    return {
        "city": weather["city"],
        "temperature_c": weather["temp_c"],
        "weather": weather["description"],
        "warm_clothes": needs_warm_clothes(weather["temp_c"]),
        "currency": currency.upper(),
        "rate_to_rub": rate,
        "expensive": is_expensive_rate(rate),
    }