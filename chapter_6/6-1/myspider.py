import scrapy
class BlogSpider(scrapy.Spider):
    # spider의 이름
    name = 'blogspider'

    # 크롤링을 시작할 URL 리스트
    start_urls = ['https://blog.scrapinghub.com']
    
    def parse(self, response):
        """
        최상위 페이지에서 카테고리 페이지의 링크를 추출합니다.
        """
        for url in response.css('ul li a::attr("href")').re('.*/category/.*'):
            yield scrapy.Request(response.urljoin(url), self.parse_titles)
    
    def parse_titles(self, response):
        """
        카페고리 페이지에서 카테고리 타이틀을 모두 추출합니다.
        """
        for post_title in response.css('div.entries > ul > li a::text').extract():
            yield {'title': post_title}