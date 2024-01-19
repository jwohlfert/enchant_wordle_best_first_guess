from math import floor, ceil

import pandas as pd

cards = pd.read_json("data/default-cards-scryfall.json").sort_values(by=["released_at"])
cards = cards[cards["set"].str.len() == 3]
print(cards.columns)
cards[["type", "subtype"]] = cards['type_line'].str.split(' — ', expand=True)

print(cards[cards["set_name"] == "Magic 2015"].type.head())

set_list = cards.set_name.unique()
if len(set_list) % 2 == 0:
    median = [set_list[int(floor(len(set_list) / 2))], set_list[int(ceil(len(set_list) / 2))]]
else:
    median = [set_list[int(len(set_list) / 2)]]
print(median)

