import csv

with open('top_cities.csv', 'w', newline='') as f:
    # 첫 번째 매개변수에 파일 객체
    # 두 번째 매개변수에 필드 이름 리스트를 지정합니다.
    writer = csv.DictWriter(f, ['rank', 'city', 'population'])
      # 첫 번째 줄에 헤더를 입력합니다.
    writer.writeheader()
    # writerows()로 여러 개의 데이터를 딕셔너리 형태로 작성합니다.
    writer.writerows([
        {'rank': 1, 'city': '상하이', 'population': 24150000},
        {'rank': 2, 'city': '카라치', 'population': 23500000},
        {'rank': 3, 'city': '베이징', 'population': 21516000},
        {'rank': 4, 'city': '텐진', 'population': 14722100},
        {'rank': 5, 'city': '이스탄불', 'population': 14160467},
    ])