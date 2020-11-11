DROP TABLE IF EXISTS bets CASCADE;
DROP TABLE IF EXISTS prices CASCADE;
DROP TABLE IF EXISTS games CASCADE;

CREATE TABLE games (
    id serial PRIMARY KEY,
    game_id INT  UNIQUE NOT NULL,
    max_rate FLOAT NOT NULL,
    total_bet_amount FLOAT NOT NULL,
    total_win_amount FLOAT NOT NULL,
    total_profit_amount FLOAT NOT NULL,
    player_count INT NOT NULL,
    bet_count INT NOT NULL,
    hash_value CHAR(64) UNIQUE NOT NULL,
    timestamp BIGINT NOT NULL,
    date TIMESTAMP NOT NULL
);

CREATE TABLE prices (
    id serial PRIMARY KEY,
    game_id INT NOT NULL UNIQUE REFERENCES games(game_id),
    based_currency VARCHAR(7) NOT NULL,
    btc FLOAT,
    etc FLOAT,
    eth FLOAT,
    xrp FLOAT,
    eos FLOAT,
    link FLOAT,
    uni FLOAT,
    doge FLOAT,
    dot FLOAT,
    ltc FLOAT,
    bch FLOAT,
    bsv FLOAT,
    avc FLOAT,
    lend FLOAT,
    mana FLOAT,
    eurs FLOAT,
    vndc FLOAT,
    xlm FLOAT,
    enj FLOAT,
    bat FLOAT,
    trx FLOAT,
    usdt FLOAT,
    vsys FLOAT,
    dai FLOAT,
    xmr FLOAT,
    trtl FLOAT,
    sero FLOAT,
    axe FLOAT,
    sog FLOAT
);

CREATE TABLE bets (
    id serial PRIMARY KEY,
    game_id INT REFERENCES games(game_id),
    user_id INT NOT NULL,
    username TEXT NOT NULL,
    bet_id  INT UNIQUE NOT NULL,
    game_type VARCHAR(6) NOT NULL,
    odds FLOAT NOT NULL,
    bet_status VARCHAR(4) NOT NULL,
    crypto_currency_name VARCHAR(5) NOT NULL,
    crypto_bet_amount FLOAT NOT NULL,
    crypto_win_amount FLOAT NOT NULL,
    crypto_profit_amount FLOAT NOT NULL,
    fiat_is_valuable BOOLEAN NOT NULL,
    fiat_currency_name VARCHAR(5),
    fiat_bet_amount FLOAT,
    fiat_win_amount FLOAT,
    fiat_profit_amount FLOAT
);