from bs4 import BeautifulSoup

# HTML 파일을 읽어 들이고 BeautifulSoup 객체를 생성합니다.
with open('full_book_list.html') as f:
    soup = BeautifulSoup(f, 'html.parser')

# find_all() 메서드로 a 요소를 추출하고 반복을 돌립니다.
for a in soup.find_all('a'):
    # href 속성과 글자를 추출합니다.
    print(a.get('href'), a.text)