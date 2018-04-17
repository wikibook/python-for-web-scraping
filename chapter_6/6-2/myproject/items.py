# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Headline(scrapy.Item):
    """
    뉴스 헤드라인을 나타내는 Item 객체
    """
    title = scrapy.Field()
    body = scrapy.Field()