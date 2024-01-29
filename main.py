import pandas as pd


def list_compare(list1, list2):
    return set(list1) == set(list2)


cards = pd.read_json("data/cards-first-printing-scryfall.json")

# find the "middle-most" set(s) chronologically
set_list = cards.set_name.unique()
middle_index = len(set_list) // 2
if len(set_list) % 2 == 0:
    median_sets = [set_list[middle_index], set_list[middle_index + 1]]
else:
    median_sets = [set_list[middle_index]]
print(f"Median Set(s):{'/'.join(median_sets)}")

# find the most common type
# Note: I have found if I go through these next few steps looking at all the cards, there may not be a card in the
# median sets that match all the criteria, so I am going to just look cards in the median sets and see where that
# gets me.
set_filter = (cards["set_name"].isin(median_sets))
type_count = cards[set_filter]["type1"].value_counts()
common_type = type_count.index[0]
print(f"Most Common Type: {common_type}")

# find the most common subtype
type_filter = set_filter & (cards["type1"] == common_type)
subtype_count = cards[type_filter]["subtype1"].value_counts()
common_subtype = subtype_count.index[0]
print(f"Most Common Subtype: {common_subtype}")

# find the most common color identity
subtype_filter = type_filter & (cards["subtype1"] == common_subtype)
color_identity_count = cards[subtype_filter]["color_identity"].value_counts(dropna=False)
common_color_identity = color_identity_count.index[0]
print(f"Most Common Color Identity: {common_color_identity}")

# find the most common rarity (probably common, but who knows based on the previous criteria)
color_identity_filter = (subtype_filter &
                         (cards["color_identity"].apply(list_compare, args=(common_color_identity,))))
rarity_count = cards[color_identity_filter]["rarity"].value_counts()
common_rarity = rarity_count.index[0]
print(f"Most Common Rarity: {common_rarity}")

full_card_filter = color_identity_filter & (cards["rarity"] == common_rarity)
print(cards[full_card_filter][["name", "cmc", "color_identity", "rarity", "type1", "subtype1", "set_name"]])
