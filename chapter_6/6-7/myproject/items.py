# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Restaurant(scrapy.Item):
    """
    서울 음식점 정보
    """
    name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    station = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()

class Page(scrapy.Item):
    """
    Web 페이지
    """
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    def __repr__(self):
        """
        로그에 출력할 때 너무 길게 출력하지 않게
        content를 생략합니다.
        """
        # 해당 페이지를 복제합니다.
        p = Page(self)
        if len(p['content']) > 100:
            # 100자 이후의 내용은 생략합니다.
            p['content'] = p['content'][:100] + '...'
        # 복제한 Page를 문자열로 만들어서 반환합니다.
        return super(Page, p).__repr__()