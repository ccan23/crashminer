#!/usr/bin/env python3

class datamodel:

    import json 

    def __init__(self, **kwargs):
        self.game_data = kwargs.get('game_data')

    def add_currency_data(self):
        data = self.game_data
        
        with open('../resources/price_list.json', 'r') as file:
            price_list = self.json.loads(file.read()) # curr_data

        data['data']['gb'].update(price_list)
        max_rate = data['data']['gb']['extend']['maxRate']
        data['data']['gb']['extend']['maxRate'] = max_rate / 100

        return data
        
    def add_player_data(self):
        data = self.add_currency_data()
        gv = data['data']['gv']
        for player in gv:
            for bet in player['bets']:
                bet['betId'] = int(bet['betId'])
                bet['betAmount'] = float(bet['betAmount'])
                bet['winAmount'] = float(bet['winAmount'])
                bet['profitAmount'] = float(bet['winAmount']) - float(bet['betAmount'])
                bet['odds'] /= 10000
                if bet['profitAmount'] > 0:
                    bet['betStatus'] = 'win'

                else: 
                    bet['betStatus'] = 'lose'

                currency = {}
                currency_name = data['data']['gb']['price']['currencyName']
                if bet['currencyName'].lower() in data['data']['gb']['price']['priceList']:
                    price = data['data']['gb']['price']['priceList'][bet['currencyName'].lower()]['price']
                    if price:
                        currency['currencyName'] = currency_name
                        currency['betAmount'] = bet['betAmount'] * price
                        currency['winAmount'] = bet['winAmount'] * price
                        currency['profitAmount'] = bet['profitAmount'] * price
                        currency['isValuable'] = True

                    else:
                        currency['isValuable'] = False

                else:
                    currency = {'isValuable': False}

                bet['currency'] = currency

        return data

    def add_total_values(self):
        bet_amount = []
        win_amount = []
        profit_amount = []

        data = self.add_player_data()
        
        bet_counter = 0

        for player in data['data']['gv']:
            for bet in player['bets']:
                bet_counter += 1

                if bet['currency']['isValuable']:
                    bet_amount.append(bet['currency']['betAmount'])
                    win_amount.append(bet['currency']['winAmount'])
                    profit_amount.append(bet['currency']['profitAmount'])
        
        total = {
            'betAmount': sum(bet_amount),
            'winAmount': sum(win_amount),
            'profitAmount': sum(profit_amount)
        }

        data['data']['gb']['total'] = total
        data['data']['gb']['playerCount'] = len(data['data']['gv'])
        data['data']['gb']['betCount'] = bet_counter

        # self.write_output(data)
        return data

    @property
    def data(self):
        return self.add_total_values()


    # @property
    # def example(self):
    #     with open('../test/datadumptest.json', 'r') as file:
    #         return self.json.loads(file.read())

    def write_output(self, data):
        with open(f"../data/{data['data']['gb']['gameId']}.json", 'w') as file:
            file.write(self.json.dumps(data))