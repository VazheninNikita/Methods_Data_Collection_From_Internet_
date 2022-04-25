import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from castorama.items import CastoramaItem

class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']


    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.category = None
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?limit=96&q={kwargs.get('query')}"]

    def parse(self, response: HtmlResponse):
        self.category = response.xpath("//h1/text()")

        next_page = response.xpath("//a[@class='next i-next']")
        if next_page:
            yield response.follow(next_page[0], callback=self.parse)

        links = response.xpath("//a[@class='product-card__img-link']")
        for link in links:
            yield response.follow(link, callback=self.castorama_parse)

    def castorama_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('name', "//h1[@itemprop='name']/text()")
        loader.add_xpath('price', "//span[@class='regular-price']//span//text()")
        loader.add_xpath('photos', "//img[contains(@class, 'top-slide__img')]/@data-src")
        loader.add_value('url', response.url)
        loader.add_xpath('attribute_label', "//div[@id='specifications']//span[contains(@class, 'specs-table__attribute-name')]/text()")
        loader.add_xpath('attribute_value', "//div[@id='specifications']//dd/text()")
        loader.add_value('category', self.category)

        yield loader.load_item()

        # name = response.xpath("//h1[@itemprop='name']/text()").get()
        # price = response.xpath("//span[@class='regular-price']//span//text()".get()
        # photos_links = response.xpath("//img[contains(@class, 'top-slide__img')]/@data-src").getall()
        # url = response.url
        # yield CastoramaItem(name=name, price=price, photos=photos_links, url=url, category=self.category)

