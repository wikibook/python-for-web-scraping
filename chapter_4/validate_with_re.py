import re
value = '3,000'

# 숫자와 쉼표만을 포함한 정규 표현식에 매치하는지 확인합니다.
if not re.search(r'^[0-9,]+$', value):
    # 값이 제대로 돼 있지 않다면 예외를 발생시킵니다.
    raise ValueError('Invalid price')