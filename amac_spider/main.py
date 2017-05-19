from scrapy.crawler import CrawlerProcess
from amac_spider.spiders.fund_spider import FundSpider
#print ("aaa")
process = CrawlerProcess()
process.crawl(FundSpider)
process.start()