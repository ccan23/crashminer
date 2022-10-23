#!/usr/bin/env python3

class crawler:

    import json
    import requests
    from datetime import datetime

    def __init__(self, gameid):
        self.gameid = gameid
        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36" }
        self.response = self.requests.get(f'https://hash.game/api/game/support/bet-log/all-bet/crash/{self.gameid}/', headers = headers)

    @property
    def data(self):
        return self.json.loads(self.response.text)

    def save_output(self, path = '../resources/datadump.json'):
        with open(path, 'w') as file:
            file.write(self.response.text)
