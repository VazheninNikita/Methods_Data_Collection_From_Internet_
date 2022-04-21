from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjobru import SuperjobruSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(HhruSpider)
    runner.crawl(SuperjobruSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()