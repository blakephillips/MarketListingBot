import json
import os
import re

import bs4
import requests


def evaluate_news_title(title) -> list:

    intent = title.find("Will List")
    symbols = re.findall("\((.*?)\)", title)

    if intent != -1 and symbols:
        print(f"New Listing: '{title}' Symbol: {symbols}")
        return symbols
    else:
        print(f"INFO: No New Listing: '{title}'")
        return None


def get_all_new_crypto_announcements() -> dict:
    r = requests.get("https://www.binance.com/en/support/announcement/c-48")
    soup = bs4.BeautifulSoup(r.content, features="html.parser")

    tag = "__APP_DATA"
    result = soup.find(id=tag).get_text()
    result_json = json.loads(result)
    result_json = result_json["routeProps"].popitem()
    new_listing_catalog = []

    for i in result_json[1]['catalogs']:
        if i['catalogId'] == 48:
            new_listing_catalog = i
            break

    return new_listing_catalog


class Binance:
    def __init__(self, root_dir):
        self.files = {}
        files = [('evaluated_ids', 'data/binance/evaluated_ids.json')]
        for file in files:
            file_name, file_dir = file
            self.files[file_name] = os.path.join(root_dir, file_dir)

        self.evaluated_ids = set()
        if os.path.isfile(self.files["evaluated_ids"]):
            with open(self.files["evaluated_ids"], 'r') as openfile:
                self.evaluated_ids = set(json.load(openfile))

        self.cache_announcements()

    def cache_announcements(self):
        articles = get_all_new_crypto_announcements()['articles']
        update_needed = False

        for article in articles:
            if article["code"] not in self.evaluated_ids:
                self.evaluated_ids.add(article["code"])
                update_needed = True

        if update_needed:
            with open(self.files["evaluated_ids"], 'w') as outfile:
                json.dump(list(self.evaluated_ids), outfile)

        print(f"Cached {len(self.evaluated_ids)} binance news post IDs.")

    def is_new_listing_announcement(self) -> list:

        articles = get_all_new_crypto_announcements()['articles']
        symbols = []
        update_needed = False

        for article in articles:
            if article["code"] not in self.evaluated_ids:
                update_needed = True

                # Add this to previously spotted ids (so it's not seen as new in the future)
                self.evaluated_ids.add(article["code"])

                print(f"NEW ARTICLE: '{article['title']}'. Evaluating if it is a new listing.")
                extract = evaluate_news_title(article['title'])
                if extract:
                    # List of new listing symbols (ex. BTC, ETH, etc)
                    symbols.extend(extract)
        if not symbols:
            print("INFO: no new binance posts")

        if update_needed: 
            # Caching the new news posts
            with open(self.files["evaluated_ids"], 'w') as outfile:
                json.dump(list(self.evaluated_ids), outfile)

        return symbols
