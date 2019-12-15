# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
from tabelog_evo.items import TabelogEvoItem

class TabelogSpider(CrawlSpider):
    """
    食べログスクレイピングスパイダー
    東京の寿司屋さんの口コミををスクレイピングする
    """
    self.store_id_num = 1
    name = 'tabelog'
    allowed_domains = ['tabelog.com']
    start_urls = ['https://tabelog.com/tokyo/rstLst/sushi/?Srt=D&SrtT=rt&sort_mode=1']

    def parse(self, response):
        """
        start_urlsに対する処理
        主にメインページの処理
        """
        soup = BeautifulSoup(response.body, 'html.parser')
        store_list = soup.find_all('a', class_='list-rst__rst-name-target')

        for store in store_list[:3]:
            item = TabelogEvoItem()
            href = store["href"]
            item['link'] = href
            request = scrapy.Request(
                href,
                callback=self.parse_detail
                )
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        """
        店の詳細ページのパーシング
        口コミページに飛ぶ
        """
        if response.status_code != requests.codes.ok:
            print(f'error:not found{ response }')
            return
        item = response.meta['item']

        # 店舗名取得
        soup = BeautifulSoup(response.body, 'html.parser')
        store_name_tag = soup.find('h2', class_='display-name')
        store_name = store_name_tag.span.string
        print('{}→店名：{}'.format(self.store_id_num, store_name.strip()), end='')
        item['store_name'] = store_name.strip()

        # お寿司屋以外を除外
        store_head = soup.find('div', class_='rdheader-subinfo') # 店舗情報のヘッダー枠データ取得
        store_head_list = store_head.find_all('dl')
        store_head_list = store_head_list[1].find_all('span')
        #print('ターゲット：', store_head_list[0].text)

        if store_head_list[0].text not in {'寿司'}:
            print('お寿司屋さんではないので処理対象外')
            self.store_id_num -= 1
            return
            

