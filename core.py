"""
How to run scrapers programmatically from a script
"""
from spiders.DmozSpider import DmozSpider
from spiders.CraigslistSpider import CraigslistSpider

# scrapy api
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings


# list of crawlers
TO_CRAWL = [DmozSpider, CraigslistSpider]

# list of crawlers that are running 
RUNNING_CRAWLERS = []

def spider_closing(spider):
    """Activates on spider closed signal"""
    log.msg("Spider closed: %s" % spider, level=log.INFO)
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
        reactor.stop()

log.start(loglevel=log.DEBUG)
for spider in TO_CRAWL:
    settings = Settings()

    # crawl responsibly
    settings.set("USER_AGENT", "Kiran Koduru (+http://kirankoduru.github.io)")
    crawler = Crawler(settings)
    crawler_obj = spider()
    RUNNING_CRAWLERS.append(crawler_obj)

    # stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(crawler_obj)
    crawler.start()

# blocks process so always keep as the last statement
reactor.run()

#####################
#####################
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

setting = get_project_settings()
process = CrawlerProcess(setting)

for spider_name in process.spiders.list():
    print ("Running spider %s" % (spider_name))
    process.crawl(spider_name,query="dvh") #query dvh is custom argument used in your scrapy

process.start()