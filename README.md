# Сводка по городу

CLI-приложение на Python для получения текущей погоды
и курса валют к российскому рублю.

## Используемые API

- Open-Meteo — погода и поиск координат города.
- Frankfurter — курсы валют.

## Установка

Требуется Python 3.12 или новее.

Создать виртуальное окружение:

```powershell
py -3.12 -m venv .venv
```

Активировать:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установить зависимости:

```powershell
python -m pip install -r requirements.txt
```

## Запуск

Погода в Москве и курс USD/RUB:

```powershell
python main.py --city Moscow
```

Курс EUR/RUB:

```powershell
python main.py --city Moscow --currency EUR
```

Вывод JSON:

```powershell
python main.py --city Moscow --json
```

## Обработка данных

- Если температура ниже 0°C, рекомендуется тёплая одежда.
- Если курс валюты превышает 100 RUB, он считается дорогим.

## Обработка ошибок

- HTTP-запросы выполняются с timeout=10 секунд.
- При временных ошибках выполняется до трёх попыток.
- Для HTTP 429 учитывается заголовок Retry-After.
- Проверяются HTTP-статусы и структура JSON.

## Коды завершения

- 0 — успешное выполнение.
- 2 — ошибка аргументов командной строки.
- 3 — город или валюта не найдены.
- 4 — внешний сервис недоступен или вернул некорректные данные.

## Структура проекта

- main.py — CLI.
- clients/http.py — HTTP-запросы и повторные попытки.
- clients/weather.py — получение погоды.
- clients/rates.py — получение курса валют.
- processing/preprocessing.py — правила обработки.
- processing/service.py — сборка сводки.