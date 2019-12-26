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
        # if (item['lunch_review'] is None or item['lunch_review'] == '') and (item['dinner_review'] is None or item['dinner_review'] == ''):
        #     raise scrapy.exceptions.DropItem('Missing value: review')

        if (item['review'] is None or item['review'] == ''):
            raise scrapy.exceptions.DropItem('Missing value: review')

        if item['store_score'] is None or item['store_score'] == '-':
            raise scrapy.exceptions.DropItem('Missing value: store_score')

        return item

# PostgreSQLへの保存
class PostgresPipeline(object):
    def open_spider(self, spider: scrapy.Spider):
        # コネクションの開始
        url = spider.settings.get('POSTGRESQL_URL')
        self.conn = psycopg2.connect(url)

    def close_spider(self, spider: scrapy.Spider):
        # コネクションの終了
        self.conn.close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        sql = "INSERT INTO posts VALUES (%s, %s)"

        curs = self.conn.cursor()
        curs.execute(sql, (item['title'], item['date']))
        self.conn.commit()

        return item
