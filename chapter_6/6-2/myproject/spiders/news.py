import scrapy

# Item의 Headline 클래스를 읽어 들입니다.
from myproject.items import Headline

class NewsSpider(scrapy.Spider):
    name = 'news'
    # 크롤링 대상 도메인 리스트
    allowed_domains = ['engadget.com']
    # 크롤링을 시작할 URL 리스트
    start_urls = ['http://engadget.com/']
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('a.o-hit__link::attr("href")').extract()
        for url in link:
            # 광고 페이지 제외
            if url.find("products") == 1: 
                continue
            # 의미 없는 페이지 제외
            if url == "#": 
                continue
            # 기사 페이지
            yield scrapy.Request(response.urljoin(url), self.parse_topics)

    def parse_topics(self, response):
        item = Headline()
        item['title'] = response.css('head title::text').extract_first()
        item['body'] = " ".join(response.css('.o-article_block p')\
            .xpath('string()')\
            .extract())
        yield item