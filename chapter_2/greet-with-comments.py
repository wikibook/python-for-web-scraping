# import 구문으로 sys 모듈을 읽어 들입니다.
import sys

# def 구문으로 greet() 함수를 정의합니다.
# 들여쓰기돼 있는 줄이 함수의 내용을 나타냅니다.
def greet(name):
    # print() 함수를 사용해 문자열을 출력합니다.
    print('Hello, {0}!'.format(name))  

# if 구문도 들여쓰기로 범위를 나타냅니다.
# sys.argv는 명령줄 매개변수를 나타내는 리스트 형식의 변수입니다.
if len(sys.argv) > 1:
    # if 구문의 조건이 참일 때
    # 변수는 정의하지 않고 곧바로 사용할 수 있습니다.
    name = sys.argv[1]
    # greet() 함수를 호출합니다.
    greet(name)
else:
    # if 구문의 조건이 거짓일 때
    # greet 함수를 호출합니다.
    greet('world')