import requests
import lxml.html
def main():
    """
    크롤러의 메인 처리
    """
    # 여러 페이지에서 크롤링할 것이므로 Session을 사용합니다.
    session = requests.Session()  
    # scrape_list_page() 함수를 호출해서 제너레이터를 추출합니다.
    response = session.get('http://www.hanbit.co.kr/store/books/new_book_list.html')
    urls = scrape_list_page(response)
    # 제너레이터는 list처럼 사용할 수 있습니다.
    for url in urls:
        print(url)

def scrape_list_page(response):
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)
    for a in root.cssselect('.view_box .book_tit a'):
        url = a.get('href')
        # yield 구문으로 제너레이터의 요소 반환
        yield url

if __name__ == '__main__':
    main()