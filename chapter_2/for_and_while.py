# 변수 x에 in의 오른쪽 리스트가 차례대로 들어갑니다.
# 따라서 블록 내부의 처리가 3번 반복됩니다.
for x in [1, 2, 3]:
    # 1, 2, 3이 차례대로 출력됩니다.
    print(x)  

# 횟수를 지정해서 반복할 때는 range()를 사용합니다
for i in range(10):
    # 0 9가 차례대로 출력됩니다.
    print(i)  

# for 구문으로 dict를 지정하면 키를 기반으로 순회합니다.
d = {'a': 1, 'b': 2}
for key in d:
    value = d[key]
    print(key, value)

# dict의 items() 메서드로 dict 키와 값을 순회합니다.
for key, value in d.items():
    print(key, value)

# while 구문으로 식이 참일 때 반복 처리합니다.
s = 1
while s < 1000:
    # # 1, 2, 4, 8, 16, 32, 64, 128, 256, 512가 차례대로 출력됩니다.
    print(s)
    s = s * 2