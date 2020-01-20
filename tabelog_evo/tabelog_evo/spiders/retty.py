# -*- coding: utf-8 -*-
import scrapy


class RettySpider(scrapy.Spider):
    name = 'retty'
    allowed_domains = ['retty.me']
    start_urls = ['http://retty.me/']

    def parse(self, response):
        pass
