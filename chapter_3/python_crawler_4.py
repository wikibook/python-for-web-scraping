import requests
import lxml.html

def main():
    # 여러 페이지에서 크롤링할 것이므로 Session을 사용합니다.
    session = requests.Session()  
    response = session.get('http://www.hanbit.co.kr/store/books/new_book_list.html')
    urls = scrape_list_page(response)
    for url in urls:
        response = session.get(url)  # Session을 사용해 상세 페이지를 추출합니다.
        ebook = scrape_detail_page(response)  # 상세 페이지에서 상세 정보를 추출합니다.
        print(ebook)  # 책 관련 정보를 출력합니다.
        break  # 책 한 권이 제대로 되는지 확인하고 종료합니다.

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
        'content': [p.text_content()\
            for p in root.cssselect('#tabs_3 .hanbit_edit_view p')]
    }
    return ebook

if __name__ == '__main__':
    main()