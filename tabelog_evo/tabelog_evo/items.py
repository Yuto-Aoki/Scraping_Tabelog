# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TabelogEvoItem(scrapy.Item):
    store_name = scrapy.Field()
    store_score = scrapy.Field()
    area = scrapy.Field()
    lunch = scrapy.Field()
    dinner = scrapy.Field()
    review_cnt = scrapy.Field()
    link = scrapy.Field()
    detail_score = scrapy.Field()
    score = scrapy.Field()
    lunch_review = scrapy.Field()
    dinner_review = scrapy.Field()
