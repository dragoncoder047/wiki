import requests

rules_to_fetch = [
    'Bliptile',
]
for rule in rules_to_fetch:
    print('fetching rule', rule)
    resp = requests.get(f'https://www.conwaylife.com/wiki/index.php?title=Rule:{rule}&action=raw')
    with open(f'Rule:{rule}', 'w') as rf:
        rf.write(resp.text)
    if len(resp.text) == 0:
        raise EOFError(f'No content for {rule}')
print('Fetched:', rules_to_fetch)
