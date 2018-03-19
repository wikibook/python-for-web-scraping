import re
import lxml.html
from pymongo import MongoClient

def scrape(key):
    """
    워커로 실행할 대상
    """
    # 로컬 호스트의 MongoDB에 접속합니다.
    client = MongoClient('localhost', 27017)

    # scraping 데이터베이스의 ebook_htmls 콜렉션을 추출합니다.
    html_collection = client.scraping.ebook_htmls

    # MongoDB에서 key에 해당하는 데이터를 찾습니다.
    ebook_html = html_collection.find_one({'key': key})
    ebook = scrape_detail_page(key, ebook_html['url'], ebook_html['html'])

    # ebooks 콜렉션을 추출합니다.
    ebook_collection = client.scraping.ebooks

    # key로 빠르게 검색할 수 있게 유니크 인덱스를 생성합니다.
    ebook_collection.create_index('key', unique=True)

    # ebook을 저장합니다.
    ebook_collection.insert_one(ebook)

def scrape_detail_page(key, url, html):
    """
    상세 페이지의 Response에서 책 정보를 dict로 추출하기
    """
    root = lxml.html.fromstring(html)
    ebook = {
        'url': response.url,
        'key': key,
        'title': root.cssselect('.store_product_info_box h3')[0].text_content(),
        'price': root.cssselect('.pbr strong')[0].text_content(),
        'content': [normalize_spaces(p.text_content())
            for p in root.cssselect('#tabs_3 .hanbit_edit_view p')
            if normalize_spaces(p.text_content()) != ""]
    }
    return ebook

def normalize_spaces(s):
    """
    연결돼 있는 공백을 하나의 공백으로 변경합니다.
    """
    return re.sub(r'\s+', ' ', s).strip()