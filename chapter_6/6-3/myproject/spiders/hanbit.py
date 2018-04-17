from scrapy.spiders import SitemapSpider

class HanbitSpider(SitemapSpider):
    name = "hanbit"
    allowed_domains = ["hanbit.co.kr"]
    # XML 사이트맵을 지정합니다.
    # robots.txt에서 Sitemap 디렉티브를 사용하고 있다면
    # robots.txt의 링크를 지정해도 됩니다.
    sitemap_urls = [
        "http://hanbit.co.kr/sitemap.xml",
    ]
    # 사이트맵 디렉티브에서 순회할 링크의 정규 표현식을 지정합니다.
    # sitemap_follow를 지정하지 않으면 모든 링크를 순회합니다.
    sitemap_follow = [
        r'post-2015-',
    ]
    # 사이트맵에 포함돼 있는 URL을 처리할 콜백을 지정합니다.
    # 규칙은 (<정규 표현식>, <처리할 콜백 함수>) 형태의 튜플을 지정합니다.
    # sitemap_rules를 지정하지 않으면 모든 URL을 parse() 메서드에 전달합니다.
    sitemap_rules = [
        (r'/2015/\d\d/\d\d/', 'parse_book'),
    ]

    def parse_post(self, response):
        # 책 페이지에서 제목을 추출합니다.
        yield {
            'title': response.css('.store_product_info_box h3::text').extract_first(),
        }