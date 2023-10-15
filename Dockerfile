# Используем образ Python
FROM python:3.9

# Установка зависимостей
RUN pip install requests psycopg2-binary statistics

# Создание рабочей директории внутри контейнера
WORKDIR /app

# Копирование всего содержимого каталога python_script в контейнер
COPY python_script /app

# Запуск скрипта при запуске контейнера
CMD ["python", "rate_from_api.py"]

