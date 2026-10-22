import argparse
import json
import sys

from clients.http import NotFoundError, ServiceUnavailableError
from processing.service import build_city_summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Сводка по городу: погода и курс валют"
    )
    parser.add_argument("--city", required=True, help="Название города")
    parser.add_argument("--currency", default="USD", help="Код валюты")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывести результат в формате JSON",
    )

    args = parser.parse_args()

    try:
        summary = build_city_summary(args.city, args.currency)

    except NotFoundError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 3

    except ServiceUnavailableError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 4

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Город: {summary['city']}")
        print(
            f"Погода: {summary['temperature_c']}°C, "
            f"{summary['weather']}"
        )
        print(
            "Тёплая одежда:",
            "да" if summary["warm_clothes"] else "нет",
        )
        print(
            f"{summary['currency']}→RUB: "
            f"{summary['rate_to_rub']:.2f}"
        )
        print(
            "Дорогой курс:",
            "да" if summary["expensive"] else "нет",
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())