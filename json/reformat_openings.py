import json

filepath = 'json/unedited_openings.json'
with open(filepath, 'r') as openings_file:
    openings = json.load(openings_file)

for opening in openings:
    opening['m'] = opening['m'].split()
    print(opening['m'])

with open('json/openings.json', 'w') as edited_openings_file:
    json.dump(openings, edited_openings_file)

print('done')
