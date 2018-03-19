import re
import sqlite3
from urllib.request import urlopen
from html import unescape

def main():
    """
    메인 처리입니다.
    fetch(), scrape(), save() 함수를 호출합니다.
    """
    html = fetch('http://www.hanbit.co.kr/store/books/full_book_list.html')
    books = scrape(html)
    save('books.db', books)

def fetch(url):
    """
    매개변수로 전달받을 url을 기반으로 웹 페이지를 추출합니다.
    웹 페이지의 인코딩 형식은 Content-Type 헤더를 기반으로 알아냅니다.
    반환값: str 자료형의 HTML
    """
    f = urlopen(url)
    # HTTP 헤더를 기반으로 인코딩 형식을 추출합니다.
    encoding = f.info().get_content_charset(failobj="utf-8")
    # 추출한 인코딩 형식을 기반으로 문자열을 디코딩합니다.
    html = f.read().decode(encoding)
    return html

def scrape(html):
    """
    매개변수 html로 받은 HTML을 기반으로 정규 표현식을 사용해 도서 정보를 추출합니다.
    반환값: 도서(dict) 리스트
    """
    books = []
    # re.findall()을 사용해 도서 하나에 해당하는 HTML을 추출합니다.
    for partial_html in re.findall(r'<td class="left"><a.*?</td>', html, re.DOTALL):
        # 도서의 URL을 추출합니다.
        url = re.search(r'<a href="(.*?)">', partial_html).group(1)
        url = 'http://www.hanbit.co.kr' + url
        # 태그를 제거해서 도서의 제목을 추출합니다.
        title = re.sub(r'<.*?>', '', partial_html)
        title = unescape(title)
        books.append({'url': url, 'title': title})
    
    return books

def save(db_path, books):
    """
    매개변수 books로 전달된 도서 목록을 SQLite 데이터베이스에 저장합니다.
    데이터베이스의 경로는 매개변수 dp_path로 지정합니다.
    반환값: None(없음)
    """
    # 데이터베이스를 열고 연결을 확립합니다.
    conn = sqlite3.connect(db_path)
    # 커서를 추출합니다.
    c = conn.cursor()
    # execute() 메서드로 SQL을 실행합니다.
    # 스크립트를 여러 번 실행할 수 있으므로 기존의 books 테이블을 제거합니다.
    c.execute('DROP TABLE IF EXISTS books')
    # books 테이블을 생성합니다.
    c.execute('''
        CREATE TABLE books (
            title text,
            url text
        )
    ''')
    # executemany() 메서드를 사용하면 매개변수로 리스트를 지정할 수 있습니다.
    c.executemany('INSERT INTO books VALUES (:title, :url)', books)
    # 변경사항을 커밋(저장)합니다.
    conn.commit()
    # 연결을 종료합니다.
    conn.close()

# python 명령어로 실행한 경우 main() 함수를 호출합니다.
# 이는 모듈로써 다른 파일에서 읽어 들였을 때 main() 함수가 호출되지 않게 하는 것입니다.
# 파이썬 프로그램의 일반적인 작성 방식입니다.
if __name__ == '__main__':
    main()