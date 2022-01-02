from pathlib import Path
custom_txt = Path('data', 'custom.txt')

with open(custom_txt, 'r') as custom:
    text = custom.readlines()
d = {}
for line in text:
    line.replace('\n', '')
    lst = line.split('=')
    (param, value) = lst
    d[param] = value

player_count = int(d['player_count'])
match_count = int(d['match_count'])
