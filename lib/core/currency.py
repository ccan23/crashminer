#!/usr/bin/env python3

class currency:

    import json
    from os import path
    from datetime import datetime, timedelta

    from pycoingecko import CoinGeckoAPI

    cg = CoinGeckoAPI()

    file_path = {
        'currencies': '../../resources/currencies.json',
        'price_list': '../../resources/price_list.json',
        'bcgame_list': '../../resources/bcgame_list.json',
    }

    def __init__(self, **kwargs):
        timestamp = kwargs.get('timestamp', self.datetime.now().timestamp())
        if len(str(timestamp)) == 13: self.timestamp = timestamp // 1000
        else: self.timestamp = timestamp
        self.update_output()

    @property
    def date(self):
        timestamp = (self.timestamp // 1000 if len(str(self.timestamp)) == 13 else self.timestamp)
        modified_date = self.datetime.utcfromtimestamp(timestamp).replace(microsecond = 0)
        is_historical = (True if self.datetime.now().date() > self.datetime.utcfromtimestamp(timestamp).date() else False)

        if is_historical:
            expire_time = modified_date + self.timedelta(days = 1)
            expire_time = expire_time.date()

        elif is_historical is False:
            expire_time = modified_date + self.timedelta(minutes = 5)
            expire_time = expire_time.replace(microsecond = 0)

        return {
            'timestamp': timestamp,
            'modifiedDate': str(modified_date),
            'expireTime': str(expire_time),
            'isHistorical': is_historical
        }

    def symbol_list(self, save_output = False, path = file_path['currencies']):
        result = {}
        for coin in self.cg.get_coins_list():
            result[coin['symbol']] = coin['id']

        if save_output:
            with open(path, 'w') as file:
                file.write(self.json.dumps(result))

        return result

    @property
    def price_list(self):
        result = {}
        date = self.datetime.strptime(self.date['modifiedDate'], '%Y-%m-%d %H:%M:%S')
        date = date.strftime('%d-%m-%Y %H:%M:%S')

        with open(self.file_path['bcgame_list'], 'r') as file:
            bcgame_list = self.json.loads(file.read())

        for symbol, id in bcgame_list.items():
            if symbol and (symbol in self.symbol_list()):
                coin_data = self.cg.get_coin_history_by_id(date = date, id = id)
                if 'market_data' in coin_data:
                    price = coin_data['market_data']['current_price']['usd']
                else:
                    price = -1
                
                result[symbol] = {'id': id, 'price': price}
        
        return result

    @property
    def data(self):
        return {
            'date': self.date,
            'price': self.price_list
        }

    def update_output(self):
        if self.path.exists(self.file_path['price_list']):
            with open(self.file_path['price_list'], 'r') as file:
                data = self.json.loads(file.read())
                expire_time = data['date']['expireTime']
                if self.datetime.fromtimestamp(self.timestamp) >= self.datetime.strptime(expire_time, '%Y-%m-%d'):
                    with open(self.file_path['price_list'], 'w') as file:
                        file.write(self.json.dumps(self.data))

        else:
            with open(self.file_path['price_list'], 'w') as file:
                file.write(self.json.dumps(self.data))