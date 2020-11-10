#!/usr/bin/env python3

class currency:

    import json
    from os import path
    from datetime import datetime, timedelta, timezone

    from pycoingecko import CoinGeckoAPI

    cg = CoinGeckoAPI()

    file_path = {
        'currencies': '../resources/currencies.json',
        'price_list': '../resources/price_list.json',
        'bcgame_list': '../resources/bcgame_list.json',
    }

    def __init__(self, **kwargs):
        timestamp = kwargs.get('timestamp', self.datetime.now().timestamp())
        if len(str(timestamp)) == 13: self.timestamp = timestamp // 1000
        else: self.timestamp = timestamp
        self.curr = kwargs.get('currency', 'usd')
        self.update_output()

    @property
    def date(self):
        modified_date = self.datetime.fromtimestamp(self.timestamp).replace(microsecond = 0)
        is_historical = (True if self.datetime.now().date() > modified_date.date() else False)

        if is_historical:
            expire_date = modified_date + self.timedelta(days = 1)
            expire_date = expire_date.replace(hour = 0, minute = 0, second = 0)
            
        elif is_historical is False:
            expire_date = modified_date + self.timedelta(minutes = 10)
            expire_date = expire_date.replace(microsecond = 0)

        api_format = modified_date.strftime('%d-%m-%Y %H:%M:%S')

        return {
            'timestamp': self.timestamp,
            'modifiedDate': str(modified_date),
            'expireDate': str(expire_date),
            'isHistorical': is_historical,
            'modifiedDateApi': api_format
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

        with open(self.file_path['bcgame_list'], 'r') as file:
            bcgame_list = self.json.loads(file.read())

        with open(self.file_path['currencies'], 'r') as file:
            symbol_list = self.json.loads(file.read())

        for symbol, id in bcgame_list.items():
            print('[STATUS] :: prices calculating')
            if id and (symbol in symbol_list):
                coin_data = self.cg.get_coin_history_by_id(date = str(self.date['modifiedDateApi']), id = id)
                if 'market_data' in coin_data:
                    price = coin_data['market_data']['current_price'][self.curr]
                
                else:
                    price = None
                
                result[symbol] = {'id': id, 'price': price}
                
        return result

    @property
    def data(self):
        return {
            'date': self.date,
            'price': {
                'currencyName': self.curr,
                'priceList': self.price_list
            }
        }

    def update_output(self):
        if self.path.exists(self.file_path['price_list']):
            with open(self.file_path['price_list'], 'r') as file:
                data = self.json.loads(file.read())
                expire_date = data['date']['expireDate']

                timestamp_date = self.datetime.fromtimestamp(self.timestamp)
                expire_date = self.datetime.strptime(expire_date, '%Y-%m-%d %H:%M:%S')

                if timestamp_date >= expire_date:
                    print('[STATUS] :: updating prices and expire date')
                    with open(self.file_path['price_list'], 'w') as file:
                        file.write(self.json.dumps(self.data))

        else:
            print('[STATUS] :: calculating prices and expire date')
            with open(self.file_path['price_list'], 'w') as file:
                file.write(self.json.dumps(self.data))