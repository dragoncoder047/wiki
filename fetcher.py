import urllib.request

rules_to_fetch = [
    'WireWorld',
]
for rule in rules_to_fetch:
    print('fetching rule', rule)
    try:
        with urllib.request.urlopen(f'https://conwaylife.com/wiki/index.php?title=Rule:{rule}&action=raw') as response:
           content = response.read()
        with open(f'Rule:{rule}', 'w') as rf:
            rf.write(content)
    except Exception as e:
        print('Error fetching rule', rule, end=' ')
        print(e)
print('Done')
