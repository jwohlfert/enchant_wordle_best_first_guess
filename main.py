import pandas as pd

cards = pd.read_json("data/default-cards-scryfall.json")
print(cards.columns)
# Setting the len of set names to 3 should eliminate the custom sets that scryfall creates behind the scenes for
#   organization of special cards
cards = cards[cards["set"].str.len() == 3]
# This line selects only the first printing of a given card, which is the printing the game cares about
cards = cards.sort_values(by=["released_at"]).drop_duplicates(subset=["name"], keep="first", ignore_index=True)
# these lines break up the type lines for one and two type cards, and isolate the type and subtype fields
cards[["type_line1", "type_line2"]] = cards['type_line'].str.split('//', expand=True)
cards[["type1", "subtype1"]] = cards['type_line1'].str.split('—', expand=True)
cards[["type2", "subtype2"]] = cards['type_line2'].str.split('—', expand=True)

# find the "middle-most" set(s) chronologically
set_list = cards.set_name.unique()
middle_index = len(set_list) // 2
if len(set_list) % 2 == 0:
    median_sets = [set_list[middle_index], set_list[middle_index + 1]]
else:
    median_sets = [set_list[middle_index]]
print(f"Median Set(s):{'/'.join(median_sets)}")

# find the most common type
type_count = cards["type1"].value_counts()
common_type = type_count.index[0]
print(f"Most Common Type: {common_type}")

# find the most common subtype
type_filter = cards["type1"] == common_type
subtype_count = cards[type_filter]["subtype1"].value_counts()
common_subtype = subtype_count.index[0]
print(f"Most Common Subtype: {common_subtype}")

# find the most common color identity
subtype_filter = (cards["type1"] == common_type) & (cards["subtype1"] == common_subtype)
color_identity_count = cards[subtype_filter]["color_identity"].value_counts()
common_color_identity = color_identity_count.index[0]
print(f"Most Common Subtype: {common_color_identity}")



