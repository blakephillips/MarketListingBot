import json

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class CoinMarketCap:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_api_details(self, parameters, url):

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print(data)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    def get_ids(self) -> dict:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
        crypto_ids = self.get_api_details({}, url)

        new_data = {}

        for crypto in crypto_ids["data"]:
            new_data[crypto["symbol"]] = crypto

        crypto_ids["data"] = new_data

        with open('data/coinmarketcap_ids.json', 'w') as outfile:
            json.dump(crypto_ids, outfile)

        return crypto_ids

    def get_ids_disk(self):
        with open('data/coinmarketcap_ids.json', 'r') as openfile:
            return json.load(openfile)

    def get_symbol_details(self, symbol):
        symbols = self.get_ids_disk()

        if not symbols or symbol not in symbols["data"]:
            symbols = self.get_ids()

            if symbol not in symbols:
                # TODO: symbol not found error
                pass

        return symbols["data"][symbol]

    def get_symbol_id(self, symbol):
        return self.get_symbol_details(symbol)["id"]

    def get_latest_quote(self, id):
        url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
        params = {"id": id}

        self.get_crypto_details(params, url)