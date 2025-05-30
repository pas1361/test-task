from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import requests_cache
from retry_requests import retry
import logging
import pytz
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

WEATHER_CODES = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Изморозь",
    51: "Лёгкая морось",
    53: "Умеренная морось",
    55: "Сильная морось",
    56: "Лёгкий ледяной дождь",
    57: "Сильный ледяной дождь",
    61: "Небольшой дождь",
    63: "Умеренный дождь",
    65: "Сильный дождь",
    66: "Лёгкий ледяной дождь",
    67: "Сильный ледяной дождь",
    71: "Небольшой снег",
    73: "Умеренный снег",
    75: "Сильный снег",
    77: "Снежные зёрна",
    80: "Небольшой ливень",
    81: "Умеренный ливень",
    82: "Сильный ливень",
    85: "Небольшой снегопад",
    86: "Сильный снегопад",
    95: "Гроза",
    96: "Гроза с градом",
    99: "Сильная гроза с градом"
}

# Картинка (имя файла) на каждый код погоды
ICON_MAP = {
    0: "clear-day",
    1: "partly-cloudy",
    2: "partly-cloudy",
    3: "overcast",
    45: "fog",
    48: "fog",
    51: "drizzle",
    53: "drizzle",
    55: "drizzle",
    56: "freezing-rain",
    57: "freezing-rain",
    61: "rain",
    63: "rain",
    65: "rain",
    66: "freezing-rain",
    67: "freezing-rain",
    71: "snow",
    73: "snow",
    75: "snow",
    77: "snow-grains",
    80: "showers",
    81: "showers",
    82: "showers",
    85: "snow-showers",
    86: "snow-showers",
    95: "thunderstorm",
    96: "thunderstorm",
    99: "thunderstorm",
}

def get_wind_direction(degrees):
    directions = ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]
    index = round(degrees / 45) % 8
    return directions[index]


def timezone_to_utc_offset(timezone_str):
    # Получаем объект временной зоны по строке
    tz = pytz.timezone(timezone_str)

    # Получаем текущую дату и время в этой временной зоне
    current_time = datetime.now(tz)

    # Получаем смещение от UTC (в минутах)
    offset_minutes = current_time.utcoffset().total_seconds() / 60

    # Преобразуем в часы и минуты
    hours = int(offset_minutes // 60)
    minutes = int(abs(offset_minutes % 60))

    # Форматируем в виде UTC+X или UTC-X
    sign = "+" if hours >= 0 else "-"
    utc_offset = f"UTC{sign}{abs(hours)}:{minutes:02d}"

    return utc_offset

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/weather/{city_name}")
async def get_weather(city_name: str):
    try:
        if not city_name or len(city_name.strip()) < 2:
            raise HTTPException(status_code=400, detail="Название города должно содержать минимум 2 символа")

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city_name,
            "count": 1,
            "language": "ru",
            "format": "json"
        }

        try:
            geo_response = retry_session.get(geo_url, params=geo_params)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
        except Exception as e:
            logger.error(f"Ошибка геокодинга: {str(e)}")
            raise HTTPException(status_code=502, detail="Сервис геокодинга временно недоступен")

        if not geo_data.get("results"):
            raise HTTPException(status_code=404, detail="Город не найден")

        location = geo_data["results"][0]
        lat, lon = location["latitude"], location["longitude"]
        timezone_str = location.get("timezone", "UTC")

        # Преобразуем в формат UTC+X
        utc_offset = timezone_to_utc_offset(timezone_str)

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "temperature_2m,weathercode,apparent_temperature,relative_humidity_2m,wind_speed_10m,wind_direction_10m",
            "timezone": "auto"
        }

        try:
            weather_response = retry_session.get(weather_url, params=weather_params)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
        except Exception as e:
            logger.error(f"Ошибка запроса погоды: {str(e)}")
            raise HTTPException(status_code=502, detail="Сервис погоды временно недоступен")

        current = weather_data.get("current_weather", {})
        hourly = weather_data.get("hourly", {})

        # Индексы для прогноза через 3 и 6 часов
        times = hourly.get("time", [])
        try:
            current_time_index = times.index(current["time"])
        except Exception:
            current_time_index = 0
        index_3h = current_time_index + 3 if current_time_index + 3 < len(times) else -1
        index_6h = current_time_index + 6 if current_time_index + 6 < len(times) else -1

        def make_forecast_block(idx):
            if idx == -1:
                return None
            return {
                "time": times[idx],
                "temperature": hourly["temperature_2m"][idx],
                "apparent_temperature": hourly.get("apparent_temperature", [None]*len(times))[idx],
                "humidity": hourly.get("relative_humidity_2m", [None]*len(times))[idx],
                "weather_code": hourly["weathercode"][idx],
                "weather_description": WEATHER_CODES.get(hourly["weathercode"][idx], "Неизвестно"),
                "icon": ICON_MAP.get(hourly["weathercode"][idx], "unknown"),
                "wind_speed": hourly.get("wind_speed_10m", [None]*len(times))[idx],
                "wind_direction": get_wind_direction(hourly.get("wind_direction_10m", [0]*len(times))[idx]),
            }

        forecast_3h = make_forecast_block(index_3h)
        forecast_6h = make_forecast_block(index_6h)

        timezone = weather_data.get("timezone", "Неизвестен")

        return JSONResponse({
            "location": {
                "name": location["name"],
                "country": location["country"],
                "latitude": lat,
                "longitude": lon,
                "timezone": timezone,
                "utc_offset": utc_offset
            },
            "current": {
                "time": current.get("time"),
                "temperature": current.get("temperature"),
                "humidity": None,  # В current_weather нет влажности, берем из hourly
                "feels_like": None,
                "weather_code": current.get("weathercode"),
                "weather_description": WEATHER_CODES.get(current.get("weathercode"), "Неизвестно"),
                "icon": ICON_MAP.get(current.get("weathercode"), "unknown"),
                "wind_speed": current.get("windspeed"),
                "wind_direction": get_wind_direction(current.get("winddirection", 0))
            },
            "hourly": hourly,
            "forecast_3h": forecast_3h,
            "forecast_6h": forecast_6h
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")