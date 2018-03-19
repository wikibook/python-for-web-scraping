import time
import re
import sys

import requests
import lxml.html
from pymongo import MongoClient
from redis import Redis
from rq import Queue

def main():
    """
    크롤러의 메인 처리
    """
    q = Queue(connection=Redis())
    # 로컬 호스트의 MongoDB에 접속
    client = MongoClient('localhost', 27017)
    # scraping 데이터베이스의 ebook_htmls 콜렉션을 추출합니다.
    collection = client.scraping.ebook_htmls
    # key로 빠르게 검색할 수 있게 유니크 인덱스를 생성합니다.
    collection.create_index('key', unique=True)
    
    session = requests.Session()
    # 목록 페이지를 추출합니다.
    response = requests.get('http://www.hanbit.co.kr/store/books/new_book_list.html')
    # 상세 페이지의 URL 목록을 추출합니다.
    urls = scrape_list_page(response)
    for url in urls:
        # URL로 키를 추출합니다.
        key = extract_key(url)
        # MongoDB에서 key에 해당하는 데이터를 검색합니다.
        ebook_html = collection.find_one({'key': key})
        # MongoDB에 존재하지 않는 경우에만 상세 페이지를 크롤링합니다.
        if not ebook_html:
            time.sleep(1)
            print('Fetching {0}'.format(url), file=sys.stderr)
            # 상세 페이지를 추출합니다.
            response = session.get(url)
            # HTML을 MongoDB에 저장합니다.
            collection.insert_one({
                'url': url,
                'key': key,
                'html': response.content,
            })
            # 큐에 잡을 주가합니다.
            # result_ttl=0을 매개변수로 지정해서
            # 태스크의 반환값이 저장되지 않게 합니다.
            q.enqueue('scraper_tasks.scrape', key, result_ttl=0)

def scrape_list_page(response):
    """
    목록 페이지의 Response에서 상세 페이지의 URL을 추출합니다.
    """
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)
    for a in root.cssselect('.view_box .book_tit a'):
        url = a.get('href')
        yield url

def extract_key(url):
    """
    URL에서 키(URL 끝의 p_code)를 추출합니다.
    """
    m = re.search(r"p_code=(.+)", url)
    return m.group(1)

if __name__ == '__main__':
    main()