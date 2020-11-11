#!/usr/bin/env python3

class bcgame:

    from datetime import datetime
    
    from crawler import crawler
    from currency import currency
    from datamodel import datamodel
    from bcdatabase import bcdatabase

    for gameid in range(3036481, 3036550):
        game = crawler(gameid)
        game = game.data
        
        time = game['data']['gb']['time']
        curr = currency(timestamp = time)
        curr.update_output()
        
        model = datamodel(game_data = game)
        data = model.data

        time = curr.get_time

        print(f"[STATUS] :: crawling : {gameid} :: {time}")
        
        bcdb = bcdatabase(game_id = gameid)

        games_data = data['data']['gb']
        bcdb.insert_games(max_rate = games_data['extend']['maxRate'], 
                            total_bet_amount = games_data['total']['betAmount'], 
                            total_win_amount = games_data['total']['winAmount'],
                            total_profit_amount = games_data['total']['profitAmount'],
                            player_count = games_data['playerCount'],
                            bet_count = games_data['betCount'],
                            hash_value = games_data['extend']['hash'],
                            timestamp = games_data['date']['timestamp'],
                            date = time)

        price_data = data['data']['gb']['price']
        bcdb.insert_prices(price_data)

        bets_data = data['data']['gv']
        
        for player in bets_data:
            user_id = player['userId']
            username = player['userName']
            for bet in player['bets']:
                bet_id = bet['betId']
                game_type = bet['type']
                odds = bet['odds']
                bet_status = bet['betStatus']
                crypto_currency_name = bet['currencyName'].lower()
                crypto_bet_amount = bet['betAmount']
                crypto_win_amount = bet['winAmount']
                crypto_profit_amount = bet['profitAmount']
                fiat_is_valuable = bet['currency']['isValuable']
                if fiat_is_valuable:
                    fiat_currency_name = bet['currency']['currencyName']
                    fiat_bet_amount = bet['currency']['betAmount']
                    fiat_win_amount = bet['currency']['winAmount']
                    fiat_profit_amount = bet['currency']['profitAmount']

                else:
                    fiat_currency_name = None
                    fiat_bet_amount = None
                    fiat_win_amount = None
                    fiat_profit_amount = None
                
                bcdb.insert_bets(user_id = user_id,
                                    username = username,
                                    bet_id = bet_id,
                                    game_type = game_type,
                                    odds = odds,
                                    bet_status = bet_status,
                                    crypto_currency_name = crypto_currency_name,
                                    crypto_bet_amount = crypto_bet_amount,
                                    crypto_win_amount = crypto_win_amount,
                                    crypto_profit_amount = crypto_profit_amount,
                                    fiat_is_valuable = fiat_is_valuable,
                                    fiat_currency_name = fiat_currency_name,
                                    fiat_bet_amount = fiat_bet_amount,
                                    fiat_win_amount = fiat_win_amount,
                                    fiat_profit_amount = fiat_profit_amount)

        bcdb.close()