# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StoreItem(scrapy.Item):
    store_id = scrapy.Field()
    store_name = scrapy.Field()
    store_score = scrapy.Field()
    station = scrapy.Field()
    lunch_price = scrapy.Field()
    dinner_price = scrapy.Field()
    address = scrapy.Field()
    phone_num = scrapy.Field()
    opening_time = scrapy.Field()
    regular_holiday = scrapy.Field()
    # link = scrapy.Field()
    
class ReviewItem(scrapy.Item):
    detail = scrapy.Field()
    score = scrapy.Field()
    lunch_review = scrapy.Field()
    dinner_review = scrapy.Field()
    store_id = scrapy.Field()

class TabelogEvoItem(scrapy.Item):
    store_id = scrapy.Field()
    store_name = scrapy.Field()
    store_score = scrapy.Field()
    station = scrapy.Field()
    lunch_price = scrapy.Field()
    dinner_price = scrapy.Field()
    address = scrapy.Field()
    phone_num = scrapy.Field()
    opening_time = scrapy.Field()
    regular_holiday = scrapy.Field()
    detail = scrapy.Field()
    score = scrapy.Field()
    url = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    ld_id = scrapy.Field()
    review = scrapy.Field()
    gender = scrapy.Field()

class RettyItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    phone_num = scrapy.Field()
    wannago = scrapy.Field()