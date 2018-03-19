# 변수를 선언합니다.
a = 1

# if 구문으로 처리를 분기합니다.
if a == 1:
    # if 구문의 식이 참일 때 실행합니다.
    print('a is 1')
elif a == 2:
    # elif 절의 식이 참일 때 실행합니다.
    print('a is 2')
else:
    # 어떠한 조건해도 해당하지 않을 때 실행합니다.
    print('a is not 1 nor 2')

# 조건문을 한 줄로 적을 수 있지만 읽기 어려우므로 사용하지 않는 것이 좋습니다.
print('a is 1' if a == 1 else 'a is not 1')