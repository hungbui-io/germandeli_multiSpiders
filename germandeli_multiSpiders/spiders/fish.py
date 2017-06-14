# -*- coding: utf-8 -*-
import scrapy
from germandeli_multiSpiders.items import GermandeliMultispidersItem
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from datetime import date


class FishSpider(scrapy.Spider):
    name = "fish"
    allowed_domains = ["germandeli.com"]
    start_urls = ['http://germandeli.com/fish']
    custom_settings = {'FILES_STORE': '/home/hung/Projects/germandeli_multiSpiders/output/fish'}

    def parse(self, response):
        urls = response.xpath('*//div[@class="category-cell-name"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request("http://www.germandeli.com/"+str(url), self.parse_page)
            print(url)

    def parse_page(self, response):
        urls = response.xpath('*//h2[@class="item-cell-name"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request("http://www.germandeli.com"+str(url), self.parse_product)
            print(url)

        next = response.xpath('*//div[@class="pagination pagination-small pull-right"]/ul/li[3]/a/@href').extract_first()
        yield scrapy.Request("http://www.germandeli.com"+str(next), self.parse_page)
        print(next)


    def parse_product(self, response):
        name_ = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        price_ = response.xpath('//*[@itemprop="price"]/text()').extract_first()
        ingredients_ = response.xpath('//*[@id="ingredients"]/text()').extract()
        description_ = response.xpath('*//div[@class="tab-pane active in"]/ul/li/text()').extract()

        image_ = response.xpath('//*[@itemprop="image"]/@src')
        image_url_ = response.xpath('//*[@itemprop="image"]/@src').extract_first()

        update_on_ = date.today().isoformat()

        yield GermandeliMultispidersItem(name=name_, price=price_, ingredients=ingredients_, description=description_,
                                         update_on=update_on_, file_urls=[image_url_])





