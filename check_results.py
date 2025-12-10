import json

with open('comprehensive_attack_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f'Total entries in comprehensive results: {len(data)}')
    print(f'Type of data: {type(data)}')
    
    # Check first few entries
    if data:
        if isinstance(data[0], list):
            print(f'First list has {len(data[0])} items')
            print(f'First item in first list: {data[0][0] if data[0] else None}')
        else:
            print(f'First entry: {data[0]}')