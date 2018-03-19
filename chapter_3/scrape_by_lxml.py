import lxml.html

# HTML 파일을 읽어 들이고, getroot() 메서드로 HtmlElement 객체를 생성합니다.
tree = lxml.html.parse('full_book_list.html')
html = tree.getroot()

# cssselect() 메서드로 a 요소의 리스트를 추출하고 반복을 돌립니다.
for a in html.cssselect('a'):
    # href 속성과 글자를 추출합니다.
    print(a.get('href'), a.text)