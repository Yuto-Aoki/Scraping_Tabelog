# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import psycopg2

# 値のバリデーションチェック
class ValidationPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if (item['lunch_review'] is None or item['lunch_review'] == '') and (item['dinner_review'] is None or item['dinner_review'] == ''):
            raise scrapy.exceptions.DropItem('Missing value: review')

        if item['store_score'] is None or item['store_score'] == '-':
            raise scrapy.exceptions.DropItem('Missing value: store_score')

        return item
