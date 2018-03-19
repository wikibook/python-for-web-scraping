import sys
from concurrent.futures import ThreadPoolExecutor
import feedparser
import requests
from bs4 import BeautifulSoup

def main():
    # URL을 추출합니다.
    d = feedparser.parse('http://www.aladin.co.kr/rss/special_new/351')
    urls = [entry.link for entry in d.entries]
    # 최대 3개의 스레드로 병렬 처리하는 Executor를 생성합니다.
    executer = ThreadPoolExecutor(max_workers=3)
    # Future 객체를 저장할 리스트를 선언합니다.
    futures = []
    for url in urls:
        # 함수의 실행을 스케줄링하고, Future 객체를 저장합니다.
        # submit()의 두 번째 이후 매개변수는 getch_and_scrape() 함수의 매개변수로써 전달됩니다.
        future = executer.submit(fetch_and_scrape, url)
        futures.append(future)
    
    for future in futures:
        # Future 객체의 결과를 출력합니다.
        print(future.result())

def fetch_and_scrape(url):
    """
    매개변수에 지정된 URL 페이지를 추출합니다.
    URL와 타이틀을 추출해서 dict 자료형으로 반환합니다.
    """
    # RSS 링크를 분석합니다.
    print('Parse Link', url.split('itemId=')[-1], file=sys.stderr)
    response_a = requests.get(url)
    soup_a = BeautifulSoup(response_a.content, 'lxml')
    book_url = soup_a.select_one('noscript').text.strip().split('\n')[-1]
    # 책 링크에 들어갑니다. 알라딘 사이트의 RSS가 이상하게 구성돼 있어서
    # 이러한 형태로 타고 들어가도록 코드를 구성했습니다.
    print('Parse Book Link', book_url.split('ISBN=')[-1], file=sys.stderr)
    response_b = requests.get(book_url)
    soup_b = BeautifulSoup(response_b.content, 'lxml')
    return {
        'url': url,
        'title': soup_b.title.text.strip(),
    }

if __name__ == '__main__':
    main()