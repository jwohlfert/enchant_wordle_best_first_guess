import pathlib

import pandas as pd
import requests

p = pathlib.Path("data/")
p.mkdir(parents=True, exist_ok=True)


def download_cards_to_dict():
    r = requests.get("https://api.scryfall.com/bulk-data/default_cards")
    file = requests.get(r.json()["download_uri"])
    return file.json()


file_dict = download_cards_to_dict()
cards = pd.DataFrame(file_dict)
# Setting the len of set names to 3 should eliminate the custom sets that scryfall creates behind the scenes for
#   organization of special cards
cards = cards[cards["set"].str.len() == 3]
# This line selects only the first printing of a given card, which is the printing the game cares about
cards = cards.sort_values(by=["released_at"]).drop_duplicates(subset=["name"], keep="first", ignore_index=True)
# these lines break up the type lines for one and two type cards, and isolate the type and subtype fields
cards[["type_line1", "type_line2"]] = cards['type_line'].str.split('//', expand=True)
cards[["type1", "subtype1"]] = cards['type_line1'].str.split('—', expand=True)
cards[["type2", "subtype2"]] = cards['type_line2'].str.split('—', expand=True)
# extract year to separate column
cards["release_year"] = pd.to_datetime(cards["released_at"]).dt.year
# save a csv of set names and release dates for reference
set_release_list = ["set_name", "released_at", "release_year"]
cards[set_release_list].drop_duplicates().to_json(p / 'set_release_dates.json', orient="records", index=False)
cards[set_release_list].drop_duplicates().to_csv(p / 'set_release_dates.csv', index=False)
main_file_column_list = ["name", "cmc", "color_identity", "rarity", "type1", "subtype1", "set_name", "released_at",
                         "release_year"]
cards[main_file_column_list].to_json(
    p / "cards-first-printing-scryfall.json", orient="records"
)
