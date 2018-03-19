import sys
import asyncio

import aiohttp
import feedparser
from bs4 import BeautifulSoup

# 최대 동시 다운로드 수를 3개로 제한하기 위한 세마포어를 생성합니다.
semaphore = asyncio.Semaphore(3)

async def main():
    # 인기 항목 RSS에서 URL 목록을 추출합니다
    d = feedparser.parse('http://www.reddit.com/r/python/.rss')
    urls = [entry.link for entry in d.entries]
    # 세션 객체를 생성합니다.
    with aiohttp.ClientSession() as session:
        # URL 개수만큼 코루틴을 생성합니다.
        coroutines = []
        for url in urls:
            coroutine = fetch_and_scrape(session, url)
            coroutines.append(coroutine)
        # 코루틴을 완료한 뒤 반복합니다.
        for coroutine in asyncio.as_completed(coroutines):
            # 코루틴 결과를 출력합니다: 간단하게 출력을 보여드리고자 가공했습니다.
            output = await coroutine
            output['url'] = output['url'].replace('https://www.reddit.com/r/Python/comments', '')
            print(output)

async def fetch_and_scrape(session, url):
    """
    매개변수로 지정한 URL과 제목을 포함한 dict를 반환합니다.
    """
    # 세마포어 락이 풀릴 때까지 대기합니다.
    with await semaphore:
        print('Start downloading', 
            url.replace('https://www.reddit.com/r/Python/comments', ''), 
            file=sys.stderr)
        # 비동기로 요청을 보내고 응답 헤더를 추출합니다.
        response = await session.get(url)
        # 응답 본문을 비동기적으로 추출합니다.
        soup = BeautifulSoup(await response.read(), 'lxml')
        return {
            'url': url,
            'title': soup.title.text.strip(),
        }
    
if __name__ == '__main__':
    # 이벤트 루프를 추출합니다.
    loop = asyncio.get_event_loop()
    # 이벤트 루프로 main()을 실행하고 종료할 때까지 대기합니다.
    loop.run_until_complete(main())