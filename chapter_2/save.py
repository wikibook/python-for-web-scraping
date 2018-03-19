import json

cities = [
    {'rank': 1, 'city': '상하이', 'population': 24150000},
    {'rank': 2, 'city': '카라치', 'population': 23500000},
    {'rank': 3, 'city': '베이징', 'population': 21516000},
    {'rank': 4, 'city': '텐진', 'population': 14722100},
    {'rank': 5, 'city': '이스탄불', 'population': 14160467},
]

print(json.dumps(cities))