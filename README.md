# 🌦️ Pas Weather Application

**Тестовое задание для О-Комплекс**

[![Docker Pulls](https://img.shields.io/docker/pulls/pas1361/pas-weather-app?style=flat-square)](https://hub.docker.com/r/pas1361/pas-weather-app)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green?style=flat-square)](https://fastapi.tiangolo.com)

## 🚀 Особенности проекта

✅ **Автодополнение городов** - интеллектуальные подсказки при вводе  
✅ **История посещений** - запоминает последний просмотренный город  
✅ **Docker контейнер** - готов к развертыванию ([Docker Hub](https://hub.docker.com/r/pas1361/pas-weather-app))  
✅ **Валидация ввода** - проверка корректности названия города  
✅ **Детальная информация**:
   - Название города и страна
   - Координаты (широта/долгота)
   - Часовой пояс (UTC)
✅ **Прогноз погоды**:
   - Текущие условия
   - Через 3 часа
   - Через 6 часов

## 🛠️ Технологический стек

- **Backend**: Python 3.9, FastAPI
- **Frontend**: HTML5, CSS3, JavaScript
- **Инфраструктура**: Docker
- **API**: Open-Meteo Weather API

## 🐳 Запуск через Docker

```bash
docker pull pas1361/pas-weather-app
docker run -d -p 8000:8000 pas1361/pas-weather-app

После запуска откройте в браузере:
Основное приложение: http://127.0.0.1:8000
Документация API: http://127.0.0.1:8000/docs

📝 Дополнительная информация
Автор: Первишко Александр
📧 Email: pervishko@alexandr.by
📞 Телефон: +7 (952) 606-66-07

Docker Hub
