# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TabelogEvoItem(scrapy.Item):
    store_id = scrapy.Field()
    store_name = scrapy.Field()
    store_score = scrapy.Field()
    area = scrapy.Field()
    lunch_price = scrapy.Field()
    dinner_price = scrapy.Field()
    review_cnt = scrapy.Field()
    link = scrapy.Field()
    points = scrapy.Field()
    score = scrapy.Field()
    lunch_review = scrapy.Field()
    dinner_review = scrapy.Field()
