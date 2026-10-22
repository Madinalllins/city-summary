from clients.http import (
    NotFoundError,
    ServiceUnavailableError,
    get_json,
)


def get_rate(currency: str = "USD") -> float:
    currency = currency.upper()

    if len(currency) != 3 or not currency.isalpha():
        raise NotFoundError("Некорректный код валюты")

    if currency == "RUB":
        return 1.0

    url = f"https://api.frankfurter.dev/v2/rate/{currency}/RUB"
    data = get_json(url)

    rate = data.get("rate")

    if not isinstance(rate, (int, float)) or isinstance(rate, bool):
        raise ServiceUnavailableError(
            "В ответе API отсутствует корректный курс"
        )

    if rate <= 0:
        raise ServiceUnavailableError("Некорректное значение курса")

    return float(rate)