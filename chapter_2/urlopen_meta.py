import re
import sys
from urllib.request import urlopen

f = urlopen('http://www.hanbit.co.kr/store/books/full_book_list.html')
# bytes 자료형의 응답 본문을 일단 변수에 저장합니다.
bytes_content = f.read()  

# charset은 HTML의 앞부분에 적혀 있는 경우가 많으므로
# 응답 본문의 앞부분 1024바이트를 ASCII 문자로 디코딩해 둡니다.
# ASCII 범위 이위의 문자는 U+FFFD(REPLACEMENT CHARACTER)로 변환되어 예외가 발생하지 않습니다.
scanned_text = bytes_content[:1024].decode('ascii', errors='replace')

# 디코딩한 문자열에서 정규 표현식으로 charset 값을 추출합니다.
match = re.search(r'charset=["\']?([\w-]+)', scanned_text)
if match:
    encoding = match.group(1)
else:
    # charset이 명시돼 있지 않으면 UTF-8을 사용합니다.
    encoding = 'utf-8'

# 추출한 인코딩을 표준 오류에 출력합니다.
print('encoding:', encoding, file=sys.stderr)

# 추출한 인코딩으로 다시 디코딩합니다.
text = bytes_content.decode(encoding)
# 응답 본문을 표준 출력에 출력합니다.
print(text)