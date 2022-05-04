import requests

rules_to_fetch = [
    'Bliptile',
    'NoTimeAtAll'
]
for rule in rules_to_fetch:
    print('fetching rule', rule)
    resp = requests.get(f'https://www.conwaylife.com/w/index.php?title=Rule:{rule}&action=raw')
    with open(f'Rule:{rule}', 'w') as rf:
        rf.write(resp.text)
    if len(resp.text) == 0:
        raise EOFError(f'Error: Rule \'{rule}\' is empty')
print('Fetched:', rules_to_fetch)
