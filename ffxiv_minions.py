import json
import requests

lodestone_id = int(input("Type your lodestone ID: "))

r = requests.get(f'https://xivapi.com/character/{lodestone_id}?data=MIMO')
lodestone_char = json.loads(r.content)
owned_minions = lodestone_char["Minions"]
r_ffxiv_collect = requests.get('https://ffxivcollect.com/api/minions')
all_minions = json.loads(r_ffxiv_collect.content)["results"]
missing_minions = []

def contains_name(array,name):
    for item in array:
        if item["Name"] == name:
            return True

    return False

for minion in all_minions:
    if not contains_name(owned_minions,minion["name"]):
        missing_minions.append({'name':minion["name"],'namesource':minion["sources"][0]["type"]})

for minion in missing_minions:
    print(f'{minion["name"]}, obtain {minion["namesource"]} ')

print("=======")
print("Owned " + str(len(owned_minions)))
print("Missing " + str(len(missing_minions)))
print("All " + str(len(all_minions)))