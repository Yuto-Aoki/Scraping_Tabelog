# Scraping Tabelog with Scrapy
このリポジトリはPythonのライブラリであるScrapyを用いて食べログの口コミを取得するためのものです。

# 動作手順
git clone {url} でこのリポジトリをクローンしてください。

- Scrapy 1.7.3
- BeautifulSoup4 4.8.1

これらのライブラリをpip installした環境で
```
cd tabelog_evo
scrapy crawl tabelog -o test.csv
```
とするとtest.csvに取得した口コミを出力します。

# データベース
