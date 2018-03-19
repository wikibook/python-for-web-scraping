import csv

# 파일을 엽니다. newline=''으로 줄바꿈 코드의 자동 변환을 제어합니다.
with open('top_cities.csv', 'w', newline='') as f:
    # csv.writer는 파일 객체를 매개변수로 지정합니다.
    writer = csv.writer(f)  
    # 첫 번째 줄에는 헤더를 작성합니다.
    writer.writerow(['rank', 'city', 'population'])  
    # writerows()에 리스트를 전달하면 여러 개의 값을 출력합니다.
    writer.writerows([
        [1, '상하이', 24150000],
        [2, '카라치', 23500000],
        [3, '베이징', 21516000],
        [4, '텐진', 14722100],
        [5, '이스탄불', 14160467],
    ])