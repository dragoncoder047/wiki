import requests

rules_to_fetch = [
    'WireWorld',
]
for rule in rules_to_fetch:
    print('fetching rule', rule)
    try:
        resp = requests.get(f'https://www.conwaylife.com/wiki/index.php?title=Rule:{rule}&action=raw')
        with open(f'Rule:{rule}', 'w') as rf:
            rf.write(resp.text)
    except Exception as e:
        print('Error fetching rule', rule, end=' ')
        print(e)
        raise SystemExit(1)
print('Fetched:', rules_to_fetch)
