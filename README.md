# 🌦️ Pas Weather Application

**Тестовое задание для О-Комплекс**

[![Docker Pulls](https://img.shields.io/docker/pulls/pas1361/pas-weather-app?style=flat-square)](https://hub.docker.com/r/pas1361/pas-weather-app)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green?style=flat-square)](https://fastapi.tiangolo.com)

## 🚀 Особенности проекта

✅ **Автодополнение городов с помощью API** — интеллектуальные подсказки при вводе города без БД.  
✅ **История посещений** — запоминает последний просмотренный город.  
✅ **Docker контейнер** — готов к развертыванию ([Docker Hub](https://hub.docker.com/r/pas1361/pas-weather-app)).  
✅ **Валидация ввода** — проверка корректности названия города.  
✅ **Адаптивная вёрстка**. 

✅ **Детальная информация о городе**:
   - Название города и страна
   - Координаты (широта/долгота)
   - Часовой пояс (UTC)
     
✅ **Прогноз погоды**:
   - Текущие условия
   - Прогноз через 3 часа
   - Прогноз через 6 часов

## 🛠️ Технологический стек

- **Backend**: Python 3.13, FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Инфраструктура**: Docker
- **API**: Open-Meteo Weather API

## 🐳 Запуск через Docker

1. Скачайте и запустите Docker контейнер:

    ```bash
    docker pull pas1361/pas-weather-app
    docker run -d -p 8000:8000 pas1361/pas-weather-app
    ```

2. После запуска откройте в браузере:

   - Основное приложение: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - Документация API: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## 📞 Контактная информация

**Автор**: Первишко Александр Сергеевич  
📧 **Email**: [pervishko@alexandr.by](mailto:pervishko@alexandr.by)  
📞 **Телефон**: [+7 (952) 606-66-07](tel:+79526066607)  
💼 **HH.RU**: ([hh.ru/resume/eb99aeccff02a967c70039ed1f42784a69374b](https://leningradskaya.hh.ru/resume/eb99aeccff02a967c70039ed1f42784a69374b))

## 🐳 Docker Hub

[![Docker Image](https://img.shields.io/badge/Docker%20Image-pas1361/pas--weather--app-2496ED?style=for-the-badge&logo=docker)](https://hub.docker.com/r/pas1361/pas-weather-app)

🔗 **Ссылка на образ**: [https://hub.docker.com/r/pas1361/pas-weather-app](https://hub.docker.com/r/pas1361/pas-weather-app)

## 📜 Лицензия

Этот проект распространяется под лицензией [MIT License](LICENSE).

---

[⬆️ Наверх](#-pas-weather-application) | [🚀 Запуск через Docker](#-запуск-через-docker)
