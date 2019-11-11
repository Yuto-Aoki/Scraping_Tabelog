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
    store_id = 0
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
            self.store_id += 1
            request = scrapy.Request(
                href,
                callback=self.parse_detail
                )
            request.meta['item'] = item
            yield request
        
        #ToDo 次ページの詳細
        # soup = BeautifulSoup(response.body, "html.parser")
        # next_page = soup.find(
        #     'a', class_="page-move__target--next")
        # if next_page:
        #     href = next_page.get('href')
        #     yield scrapy.Request(href, callback=self.parse)

    def parse_detail(self, response):
        """
        店の詳細ページのパーシング
        口コミページに移行
        """
        # if response.status_code != requests.codes.ok:
        #     print(f'error:not found{ response }')
        #     return
        item = response.meta['item']

        # 店舗名取得
        soup = BeautifulSoup(response.body, 'html.parser')
        store_name_tag = soup.find('h2', class_='display-name')
        store_name = store_name_tag.span.string
        print('{}→店名：{}'.format(self.store_id, store_name.strip()), end='')
        item['store_name'] = store_name.strip()

        # お寿司屋以外を除外
        store_head = soup.find('div', class_='rdheader-subinfo') # 店舗情報のヘッダー枠データ取得
        store_head_list = store_head.find_all('dl')
        store_head_list = store_head_list[1].find_all('span')
        #print('ターゲット：', store_head_list[0].text)

        if store_head_list[0].text not in {'寿司'}:
            print('お寿司屋さんではないので処理対象外')
            self.store_id -= 1
            return
        
        # 評価点数取得
        rating_score_tag = soup.find('b', class_='c-rating__val')
        rating_score = rating_score_tag.span.string
        print('  評価点数：{}点'.format(rating_score), end='')
        item['store_score'] = rating_score

        # 評価点数が存在しない店舗は除外
        if rating_score == '-':
            print('  評価がないため処理対象外')
            self.store_id -= 1
            return
        
        landd_tag = soup.find('div', class_='rstinfo-table__budget')
        
        lunch = landd_tag.find('em', class_='gly-b-lunch')
        dinner = landd_tag.find('em', class_='gly-b-dinner')
        try:
            item['lunch_price'] = lunch.string
        except:
            item['lunch_price'] = ''
        try:
            item['dinner_price'] = dinner.string
        except:
            item['dinner_price'] = ''
        
        #print('　昼：{} 夜：{}'.format(self.lunch_price, self.dinner_price), end='')

        # レビュー一覧URL取得
        #<a class="mainnavi" href="https://tabelog.com/tokyo/A1304/A130401/13143442/dtlrvwlst/"><span>口コミ</span><span class="rstdtl-navi__total-count"><em>60</em></span></a>
        review_tag_id = soup.find('li', id="rdnavi-review")
        review_tag = review_tag_id.a.get('href')

        # レビュー件数取得
        print('  レビュー件数：{}'.format(review_tag_id.find('span', class_='rstdtl-navi__total-count').em.string), end='')
        item['review_cnt'] = review_tag_id.find('span', class_='rstdtl-navi__total-count').em.string
        
        request = scrapy.Request(
                review_tag,
                callback=self.parse_review
                )
        request.meta['item'] = item
        yield request


    def parse_review(self, response):
        """
        口コミ一覧ページのパーシング
        口コミ詳細ページに移行
        """
        #r = requests.get(response)
        # if response.status_code != requests.codes.ok:
        #     print(f'error:not found{ response }')
        #     return
        item = response.meta['item']

        soup = BeautifulSoup(response.body, 'html.parser')

        review_url_list = soup.find_all('div', class_='rvw-item') # 口コミ詳細ページURL一覧
        
        if len(review_url_list) == 0:
            return

        for url in review_url_list:
            review_detail_url = 'https://tabelog.com' + url.get('data-detail-url')
            #print('\t口コミURL：', review_detail_url)
            request = scrapy.Request(
                review_detail_url,
                callback=self.get_review_text
                )
            request.meta['item'] = item
            yield request
            # 口コミのテキストを取得
        

    def get_review_text(self, response):
        """
        口コミ詳細ページのパーシング
        次の口コミへ
        """
        # if response.status_code != requests.codes.ok:
        #     print(f'error:not found{ response }')
        #     return
        item = response.meta['item']

        soup = BeautifulSoup(response.body, 'html.parser')

        review_block = soup.find_all('div', class_='rvw-item__review-contents')
        time_tag = response.css('strong.c-rating__time::text').getall()
        score_tag = soup.find_all('p', class_='rvw-item__single-ratings-total')
        time_list = response.css('ul.rvw-item__single-ratings-dtlscore li strong::text').getall()
        time_tag = [time_list[x:x+5] for x in list(range(0,len(time_list),5))]
        for time, score, point, review in zip():
        
        # title = soup.find('p', class_='rvw-item__title')
        # item['title'] = title.string

        # 評価の内訳取得
        # 料理味、サービス、雰囲気、CP、酒ドリンク
        points = soup.find('ul', class_='rvw-item__ratings-dtlscore')
        self.points = []
        for li in points.find_all('li'):
            self.points.append(li.strong.text)
        if len(self.points) < 5:
            self.points = ['-', '-', '-', '-', '-']
        # self.cuisine = self.points[0]
        # self.service = self.points[1]
        # self.atmos = self.points[2]
        # self.cp = self.points[3]
        # self.drink = self.points[4]
        # #print('\n料理: {} サービス: {} 雰囲気: {} CP: {} 酒: {}'.format(self.cuisine, self.service, self.atmos, self.cp, self.drink), end='')

        # score_tag = soup.find('p', class_='rvw-item__single-ratings-total')
        # score = score_tag.b.string
        # #print(' 口コミ評価点数：{}点'.format(score))
        # self.score = score

        # # 評価点数が存在しない店舗は除外
        # # if score == '-':
        # #     print('  評価がないため処理対象外')
        # #     self.store_id_num -= 1
        # #     return
        
        # print("{}個めの口コミ取得完了".format(self.i))
        # # Review取得
        # review = soup.find_all('div', class_='rvw-item__rvw-comment')#reviewが含まれているタグの中身をすべて取得
        # if len(review) == 0:
        #     review = ''
        # else:
        #     review = review[0].p.text.strip() # strip()は改行コードを除外する関数
        #     # reviewの1回目訪問のみ取得、複数取得するためにはfor i in range(len(review))でいけるはず...

        # #print('\t\t口コミテキスト：', review)
        # #self.review = review
        # if self.lunch:
        #     self.lunch_review = review
        #     self.dinner_review = ''
        
        # if self.dinner:
        #     self.lunch_review = ''
        #     self.dinner_review = review

        yield item




            


