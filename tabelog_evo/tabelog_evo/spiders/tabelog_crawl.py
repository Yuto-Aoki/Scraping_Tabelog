# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tabelog_evo.items import TabelogEvoItem

class TabelogCrawlSpider(CrawlSpider):
    name = 'tabelog_crawl'
    allowed_domains = ['tabelog.com']
    start_urls = ['https://tabelog.com/tokyo/rstLst/sushi/?Srt=D&SrtT=rt&sort_mode=1']

    rules = (
        # お店一覧をたどる
        Rule(LinkExtractor(allow=r'https://tabelog.com/tokyo/rstLst/sushi/[1-5]/')),
        # お店の詳細ページ
        Rule(LinkExtractor(allow=r'https://tabelog.com/tokyo/A\d+/A\d+/\d+/$')),
        # 口コミ一覧ページ
        Rule(LinkExtractor(allow=r'https://tabelog.com/tokyo/A\d+/A\d+/\d+/dtlrvwlst/COND-0/smp1/?smp=1&lc=0&rvw_part=all&PG=\d+'), callback='get_review_text')
    )

    def get_review_text(self, response):
        """
        口コミ詳細ページのパーシング
        次の口コミへ
        """
        # お店の名前
        name = response.css('h2.display-name').xpath('string()').get().strip()
        # お店の評価
        store_score = response.css('b.c-rating__val').xpath('string()').get().strip()
        # 各口コミの時間帯、スコア、詳細、本文を取得する
        # 時間帯のリスト　dinner: or lunch:
        time_list = response.css('strong.c-rating__time::text').getall()
        # 口コミのスコアリスト 5.0など
        score_list = response.css('p.c-rating.rvw-item__single-ratings-total > b.c-rating__val.c-rating__val--strong::text').getall()
        # 評価の内訳　5個ずつ格納
        dtl_tag = response.css('ul.rvw-item__single-ratings-dtlscore li strong::text').getall()
        dtl_list = [dtl_tag[x:x+5] for x in list(range(0,len(dtl_tag),5))]
        # 本文の取得
        # 「おすすめポイント」は口コミではないので除く
        review_list = response.css('div.rvw-item__rvw-comment p').xpath('string()').getall()
        recommend = response.css('div.rvw-item__review-contents--recommend').getall()
        if recommend:
            review_list = review_list[len(recommend)*2:]
        # 時間帯、スコア、詳細には下部の余分なものも含まれているため、除く
        cnt = len(review_list)
        for time, score, detail, review in zip(time_list[:cnt], score_list[:cnt], dtl_list[:cnt], review_list):
            item = TabelogEvoItem()
            item['store_name'] = name
            item['store_score'] = store_score
            item['score'] = score
            item['detail'] = detail
            if time == 'lunch:' or time == '昼:':
                item['lunch_review'] = review
                item['dinner_review'] = ''
            elif time == 'dinner:' or time == '夜:':
                item['lunch_review'] = ''
                item['dinner_review'] = review
            yield item
