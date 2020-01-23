# -*- coding: utf-8 -*-
import scrapy
from ..middlewares import close_driver
from tabelog_evo.items import RettyItem

class RettySpider(scrapy.Spider):
    name = 'retty'
    allowed_domains = ['retty.me']
    start_urls = ['https://retty.me/restaurant-search/search-result/?&category_type=30&min_budget=1&max_budget=13&free_word_category=%E5%AF%BF%E5%8F%B8']
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "tabelog_evo.middlewares.SeleniumMiddleware": 0,
        },
    }

    def parse(self, response):
        url_list = response.css('a.restaurant__block-link::attr("href")').getall()
        for url in url_list:
            item = RettyItem()
            item['url'] = url
            request = scrapy.Request(
                url,
                callback=self.parse_store
                )
            request.meta['item'] = item
            yield request
        self.closed()
    
    def parse_store(self, response):
        item = response.meta['item']

        

    def closed(self):
        close_driver()