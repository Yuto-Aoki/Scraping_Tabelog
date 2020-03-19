from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

settings.set('FEED_URI', 'results_%(filename)s.csv')

configure_logging()
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    yield runner.crawl('tabelog', filename='tabelog')
    yield runner.crawl('retty', page_limit=1, filename='retty')
    reactor.stop()


crawl()
reactor.run()