# sys 모듈을 현재 이름 공간으로 읽어 들입니다.
import sys 

# datetime 모듈에서 date 클래스를 읽어 들입니다.
from datetime import date

# sys 모듈의 argv라는 변수로 명령줄 매개변수 리스트를 추출하고 출력합니다.
print(sys.argv)
# date 클래스의 today() 메서드로 현재 날짜를 추출합니다.
print(date.today())