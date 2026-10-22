import time

import requests


class ServiceUnavailableError(Exception):
    pass


class NotFoundError(Exception):
    pass


RETRY_STATUSES = {429, 500, 502, 503, 504}


def get_json(url: str, params: dict | None = None) -> dict:
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=10,
            )

            if response.status_code in RETRY_STATUSES:
                if attempt < 2:
                    delay = 1

                    if response.status_code == 429:
                        retry_after = response.headers.get("Retry-After")
                        if retry_after:
                            try:
                                delay = max(0, float(retry_after))
                            except ValueError:
                                pass

                    time.sleep(delay)
                    continue

                raise ServiceUnavailableError(
                    f"Сервис недоступен: HTTP {response.status_code}"
                )

            if response.status_code in {400, 404, 422}:
                raise NotFoundError("Город или валюта не найдены")

            response.raise_for_status()

            try:
                data = response.json()
            except ValueError as exc:
                raise ServiceUnavailableError(
                    "Сервис вернул некорректный JSON"
                ) from exc

            if not isinstance(data, dict):
                raise ServiceUnavailableError(
                    "Сервис вернул неожиданный формат данных"
                )

            return data

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError) as exc:
            if attempt == 2:
                raise ServiceUnavailableError(
                    "Сервис недоступен после трёх попыток"
                ) from exc

        except requests.exceptions.RequestException as exc:
            raise ServiceUnavailableError(
                "Ошибка внешнего сервиса"
            ) from exc

    raise ServiceUnavailableError("Не удалось получить ответ")