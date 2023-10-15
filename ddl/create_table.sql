DROP TABLE IF EXISTS history_rate_btc_rub;

-- Создание таблицы для austin_bikeshare_trips.csv
CREATE TABLE IF NOT EXISTS history_rate_btc_rub (
    id SERIAL PRIMARY KEY,
    date_rate DATE,
    currencie_form CHAR(3) DEFAULT 'BTC',
    currencie_to CHAR(3) DEFAULT 'RUB',
    value_rate FLOAT
);
