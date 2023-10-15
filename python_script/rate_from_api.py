import requests
import psycopg2
from statistics import mean


def pipeline(url: str, params: dict, host: str = 'db', database: str = 'history_rate',
                       user: str = 'postgres', password: str = 'postgres'):
    history = get_rate_from_api(url, params)
    save_history_to_postgresql(history, host, database, user, password)
    calculate_statistics(host, database, user, password)

    return 0


def get_rate_from_api(url: str, params: dict) -> dict:
    response = requests.get(url, params=params)
    history = response.json()
    return history


def save_history_to_postgresql(history: dict, host: str, database: str, user: str, password: str):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(host=host,
                            database=database,
                            user=user,
                            password=password)
    cur = conn.cursor()

    # Вставка данных в базу данных
    for date, quote in history['quotes'].items():
        date_rate = date
        value_rate = quote['BTCRUB']
        cur.execute("INSERT INTO history_rate_btc_rub (date_rate, value_rate) VALUES (%s, %s)", (date_rate, value_rate))

    # Завершение транзакции и закрытие соединения
    conn.commit()
    cur.close()
    conn.close()
    return 0


def calculate_statistics(host: str = 'db', database: str = 'history_rate',
                         user: str = 'postgres', password: str = 'postgres'):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(host='db', database='history_rate', user='postgres', password='postgres')
    cur = conn.cursor()

    # Рассчитываем статистику
    cur.execute("SELECT date_rate, value_rate FROM history_rate_btc_rub")
    data = cur.fetchall()

    max_date = max(data, key=lambda x: x[1])
    min_date = min(data, key=lambda x: x[1])
    max_value = max(data, key=lambda x: x[1])[1]
    min_value = min(data, key=lambda x: x[1])[1]
    average_value = mean([x[1] for x in data])
    last_day_value = data[-1][1]

    # Создание новой таблицы
    cur.execute("CREATE TABLE IF NOT EXISTS statistics (id SERIAL PRIMARY KEY, max_date DATE, min_date DATE, max_value FLOAT, min_value FLOAT, average_value FLOAT, last_day_value FLOAT, currency_from CHAR(3), currency_to CHAR(3), month CHAR(7))")

    # Вставка данных в таблицу statistics
    cur.execute("INSERT INTO statistics (max_date, min_date, max_value, min_value, average_value, last_day_value, currency_from, currency_to, month) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (max_date[0], min_date[0], max_value, min_value, average_value, last_day_value, 'BTC', 'RUB', '2023-09'))
    
    # Завершение транзакции и закрытие соединения
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    url = 'http://api.exchangerate.host/timeframe'
    params = {'access_key': 'b56fa97aaac1908f5b8f9943cd9a02e5',
              'source': 'BTC',
              'currencies': 'RUB',
              'start_date': '2023-09-01',
              'end_date': '2023-09-30'} 
    host = 'db'
    database = 'history_rate'
    user = 'postgres'
    password = 'postgres'
    pipeline(url, params, host, database, user, password)
