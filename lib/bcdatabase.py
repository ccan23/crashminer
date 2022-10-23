#!/usr/bin/env python3

class bcdatabase:

    import psycopg2

    def __init__(self, **kwargs):
        self.con = self.psycopg2.connect(
            host = 'localhost',
            database = 'gamblers',
            user = 'postgres',
            password = 'postgres25853266414'
        )
        self.cur = self.con.cursor()
        self.game_id = kwargs.get('game_id')

    def drop_table(self, table_name):
        self.cur.execute('drop table %s;', (table_name))
        self.con.commit()
        self.con.close()
    
    def create_tables(self):
        with open('../database/create_tables.sql', 'r') as file:
            script = file.read()

        self.cur.execute(script)
        self.con.commit()

    def insert_games(self, **kwargs):
        max_rate = kwargs.get('max_rate')
        total_bet_amount = kwargs.get('total_bet_amount')
        total_win_amount = kwargs.get('total_win_amount')
        total_profit_amount = kwargs.get('total_profit_amount')
        player_count = kwargs.get('player_count')
        bet_count = kwargs.get('bet_count')
        hash_value = kwargs.get('hash_value')
        timestamp = kwargs.get('timestamp')
        date = kwargs.get('date')
        
        self.cur.execute("""INSERT INTO games (game_id, max_rate, total_bet_amount, total_win_amount, total_profit_amount, player_count, bet_count, hash_value, timestamp, date)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (self.game_id,
                                                                                        max_rate,
                                                                                        total_bet_amount,
                                                                                        total_win_amount,
                                                                                        total_profit_amount,
                                                                                        player_count,
                                                                                        bet_count,
                                                                                        hash_value,
                                                                                        timestamp,
                                                                                        date))
        self.con.commit()

    def insert_prices(self, data):
        prices = []
        prices.append(self.game_id)
        prices.append(data['currencyName'])
        data = data['priceList']
        for val in data.values():
            prices.append(val['price'])

        prices = tuple(prices)
        self.cur.execute("""INSERT INTO prices (game_id, based_currency, btc, etc, eth, xrp, eos, link, uni, doge, dot, ltc, bch,
                                                bsv, avc, lend, mana, eurs, vndc, xlm, enj, bat, trx, usdt,
                                                vsys, dai, xmr, trtl, sero, axe, sog) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )""", prices)
        self.con.commit()

    def insert_bets(self, **kwargs):
        user_id = kwargs.get('user_id')
        username = kwargs.get('username')
        bet_id = kwargs.get('bet_id')
        game_type = kwargs.get('game_type')
        odds = kwargs.get('odds')
        bet_status = kwargs.get('bet_status')
        crypto_currency_name = kwargs.get('crypto_currency_name')
        crypto_bet_amount = kwargs.get('crypto_bet_amount')
        crypto_win_amount = kwargs.get('crypto_win_amount')
        crypto_profit_amount = kwargs.get('crypto_profit_amount')
        fiat_is_valuable = kwargs.get('fiat_is_valuable')
        fiat_currency_name = kwargs.get('fiat_currency_name')
        fiat_bet_amount = kwargs.get('fiat_bet_amount', None)
        fiat_win_amount = kwargs.get('fiat_bet_amount', None)
        fiat_profit_amount = kwargs.get('fiat_profit_amount', None)

        self.cur.execute("""INSERT INTO bets (game_id, user_id, username, bet_id, game_type, odds, bet_status,
                                                crypto_currency_name, crypto_bet_amount,
                                                crypto_win_amount, crypto_profit_amount,
                                                fiat_is_valuable, fiat_currency_name,
                                                fiat_bet_amount, fiat_win_amount, fiat_profit_amount)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(self.game_id,
                                                                                                            user_id,
                                                                                                            username,
                                                                                                            bet_id,
                                                                                                            game_type,
                                                                                                            odds,
                                                                                                            bet_status,
                                                                                                            crypto_currency_name,
                                                                                                            crypto_bet_amount,
                                                                                                            crypto_win_amount,
                                                                                                            crypto_profit_amount,
                                                                                                            fiat_is_valuable,
                                                                                                            fiat_currency_name,
                                                                                                            fiat_bet_amount,
                                                                                                            fiat_win_amount,
                                                                                                            fiat_profit_amount))
        self.con.commit()

    def close(self):
        self.con.close()

# # temp data
# example_data = {'currencyName': 'usd','priceList': {'btc': {'id': 'bitcoin', 'price': 15496.316149147417}, 'etc': {'id': 'ethereum-classic', 'price': 5.203057881040663}, 'eth': {'id': 'ethereum', 'price': 455.3583669721691}, 'xrp': {'id': 'ripple', 'price': 0.2536826612170206}, 'eos': {'id': 'eos', 'price': 2.5378409518986964}, 'link': {'id': 'chainlink', 'price': 12.746094928454907}, 'uni': {'id': 'uniswap', 'price': 2.8768344518769315}, 'doge': {'id': 'dogecoin', 'price': 0.0026813962915643638}, 'dot': {'id': 'polkadot', 'price': 4.36318980541015}, 'ltc': {'id': 'litecoin', 'price': 61.028779208119225}, 'bch': {'id': 'bitcoin-cash', 'price': 271.32368033322507}, 'bsv': {'id': 'bitcoin-cash-sv', 'price': 166.96726011756684}, 'avc': {'id': 'avccoin', 'price': None}, 'lend': {'id': 'aave-lend', 'price': None}, 'mana': {'id': 'decentraland', 'price': 0.08608097759363154}, 'eurs': {'id': 'stasis-eurs', 'price': 1.194978226086445}, 'vndc': {'id': 'vndc', 'price': 4.3055070023260736e-05}, 'xlm': {'id': 'stellar', 'price': 0.08161771966431738}, 'enj': {'id': 'enjincoin', 'price': 0.13669515197826873}, 'bat': {'id': 'basic-attention-token', 'price': 0.19876883439483287}, 'trx': {'id': 'tron', 'price': 0.02537712502359173}, 'usdt': {'id': 'tether', 'price': 1.0001778796043215}, 'vsys': {'id': 'v-systems', 'price': 0.014825926082643456}, 'dai': {'id': 'dai', 'price': 1.0079874730972407}, 'xmr': {'id': 'monero', 'price': 120.4490553872958}, 'trtl': {'id': 'turtlecoin', 'price': 8.823921894444767e-06}, 'sero': {'id': 'super-zero', 'price': 0.11170971505965276}, 'axe': {'id': 'axe', 'price': 0.08570302177273244}, 'sog': {'id': 'soulgame', 'price': None}}}
# # #

# bcdb = bcdatabase(game_id = 3036433)
# bcdb.create_tables()
# bcdb.insert_games(
#                     max_rate = 3.6,
#                     total_bet_amount = 78.95713019204838,
#                     total_win_amount = 16.47176529642491,
#                     total_profit_amount = -62.48536489562344,
#                     player_count = 274,
#                     bet_count = 292,
#                     hash_value = '37eef60a2c68f05c980e8554f9438b4552b87293dd8730014926980191bc61c7',
#                     timestamp = 1604960039,
#                     date = '2020-11-09 17:13:59')
# bcdb.insert_prices(example_data)
# bcdb.insert_bets(user_id = 1415186,
#                     username = 'Olivoily',
#                     bet_id = 284457049,
#                     type = 'normal',
#                     odds = 2.0,
#                     crypto_currency_name = 'trtl',
#                     crypto_bet_amount = 8,
#                     crypto_win_amount = 16,
#                     crypto_profit_amount = 8,
#                     fiat_currency_name = 'usd',
#                     fiat_is_valuable = True,
#                     fiat_bet_amount = 7.059137515555814e-5,
#                     fiat_win_amount = .00014118275031111627,
#                     fiat_profit_amount = 7.059137515555814e-5)
# bcdb.close()
