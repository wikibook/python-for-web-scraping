import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from myproject.items import Restaurant

class VisitSeoulSpider(CrawlSpider):
    name = "visitseoul"
    allowed_domains = ["korean.visitseoul.net"]
    start_urls = ['http://korean.visitseoul.net/eat?curPage=1']
    rules = [
        # 9페이지까지 순회합니다.
        # 정규 표현식 \d를 \d+로 지정하면 모든 페이지를 순회합니다.
        Rule(LinkExtractor(allow=r'/eat\?curPage=\d$')),
        # 음식점 상세 페이지를 분석합니다.
        Rule(LinkExtractor(allow=r'/eat/\w+/\d+'),
             callback='parse_restaurant'),
    ]

    def parse_restaurant(self, response):
        """
        음식점 정보 페이지를 파싱합니다.
        """
        # 정보를 추출합니다.
        name = response.css("#pageheader h3")\
            .xpath("string()").extract_first().strip()
        address = response.css("dt:contains('주소') + dd")\
            .xpath("string()").extract_first().strip()
        phone = response.css("dt:contains('전화번호') + dd")\
            .xpath("string()").extract_first().strip()
        station = response.css("th:contains('지하철') + td")\
            .xpath("string()").extract_first().strip()
        
        # 위도 경도를 추출합니다.
        try:
            scripts = response.css("script:contains('var lat')").xpath("string()").extract_first()
            latitude = re.findall(r"var lat = '(.+)'", scripts)[0]
            longitude = re.findall(r"var lng = '(.+)'", scripts)[0]
        except Exception as exception:
            print("예외 발생")
            print(exception)
            print()
            
        # 음식점 객체를 생성합니다.
        item = Restaurant(
            name=name,
            address=address,
            phone=phone,
            latitude=latitude,
            longitude=longitude,
            station=station
        )
        yield item