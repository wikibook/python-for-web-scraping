from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# Item의 Headline 클래스를 읽어 들입니다.
from myproject.items import Headline

class NewsSpider(scrapy.Spider):
    name = 'news'
    # 크롤링 대상 도메인 리스트
    allowed_domains = ['engadget.com']
    # 크롤링을 시작할 URL 리스트
    start_urls = ['http://engadget.com/']
    # 링크 순회를 위한 규칙 리스트
    rules = [
        # 토픽 페이지를 추출한 뒤 응답을 parse_topics() 메서드에 전달합니다.
        Rule(LinkExtractor(allow=r'/\d{4}/\d{2}/\d{2}/.+$'), callback='parse_topics'),
    ]

    def parse_topics(self, response):
        item = Headline()
        item['title'] = response.css('head title::text').extract_first()
        item['body'] = " ".join(response.css('.o-article_block p')\
            .xpath('string()')\
            .extract())
        yield item