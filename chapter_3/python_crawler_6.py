import time # time 모듈을 임포트합니다.
import re 
import requests
import lxml.html

def main():
    session = requests.Session()
    response = session.get('http://www.hanbit.co.kr/store/books/new_book_list.html')
    urls = scrape_list_page(response)
    for url in urls:
        time.sleep(1) # 1초 동안 휴식합니다.
        response = session.get(url)
        ebook = scrape_detail_page(response)
        print(ebook)

def scrape_list_page(response):
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)
    for a in root.cssselect('.view_box .book_tit a'):
        url = a.get('href')
        yield url

def scrape_detail_page(response):
    """
    상세 페이지의 Response에서 책 정보를 dict로 추출합니다.
    """
    root = lxml.html.fromstring(response.content)
    ebook = {
        'url': response.url,
        'title': root.cssselect('.store_product_info_box h3')[0].text_content(),
        'price': root.cssselect('.pbr strong')[0].text_content(),
        'content': [normalize_spaces(p.text_content())
            for p in root.cssselect('#tabs_3 .hanbit_edit_view p')
            if normalize_spaces(p.text_content()) != '']
    }
    return ebook

def normalize_spaces(s):
    """
    연결돼 있는 공백을 하나의 공백으로 변경합니다.
    """
    return re.sub(r'\s+', ' ', s).strip()

if __name__ == '__main__':
    main()