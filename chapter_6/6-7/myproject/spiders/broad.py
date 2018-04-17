import scrapy
from myproject.items import Page
from myproject.utils import get_content

class BroadSpider(scrapy.Spider):
    name = "broad"
    start_urls = (
        # 하테나 북마크 엔트리 페이지
        'http://b.hatena.ne.jp/entrylist',
    )
    
    def parse(self, response):
        """
        하테나 북마크의 엔트리 페이지를 파싱합니다.
        """
        # 각각의 웹 페이지 링크를 추출합니다.
        for url in response.css('a.entry-link::attr("href")').extract():
            # parse_page() 메서드를 콜백 함수로 지정합니다.
            yield scrapy.Request(url, callback=self.parse_page)
        # of 뒤의 숫자를 두 자리로 지정해 5페이지(첫 페이지, 20, 40, 60, 80)만 추출하게 합니다.
        url_more = response.css('a::attr("href")').re_first(r'.*\?of=\d{2}$')
        if url_more:
            # url_more의 값은 /entrylist로 시작하는 상대 URL이므로
            # response.urljoiin() 메서드를 사용해 절대 URL로 변경합니다.
            # 콜백 함수를 지정하지 않았으므로 응답은 기본적으로
            # parse() 메서드에서 처리하게 됩니다.
            yield scrapy.Request(response.urljoin(url_more))
    
    def parse_page(self, response):
        """
        각 페이지를 파싱합니다.
        """
        # utils.py에 정의돼 있는 get_content() 함수로 타이틀과 본문을 추출합니다.
        title, content = get_content(response.text)
        # Page 객체로 반환합니다.
        yield Page(url=response.url, title=title, content=content)