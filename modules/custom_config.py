from modules.paths import custom_txt
from modules.text_functions import split

with open(custom_txt, 'r') as custom:
    text = custom.readlines()
d = {}
for line in text:
    lst = split(line, '=')
    (param, value) = lst
    d[param] = value

player_count = int(d['player_count'])
match_count = int(d['match_count'])
has_additional = d['has_additional'] == "True"
