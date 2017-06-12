# -*- coding: utf-8 -*-
import scrapy
from germandeli_multiSpiders.items import GermandeliMultispidersItem
from scrapy.selector import Selector
from scrapy_splash import SplashRequest


class BeveragesSpider(scrapy.Spider):
    name = "beverages"
    allowed_domains = ["germandeli.com"]
    start_urls = ['http://www.germandeli.com/Beverages']

    # def parse(self, response):
    #     category_links = response.xpath('*//ul[@class="nav"]/li/a/@href').extract()
    #     for link in category_links:
    #         yield scrapy.Request("http://germandeli.com"+link, self.parse_page)
    #         print(link)

    def parse(self, response):
        urls = response.xpath('*//div[@class="category-cell-name"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request("http://www.germandeli.com/"+url, self.parse_page)
            print(url)

    def parse_page(self, response):
        urls = response.xpath('*//h2[@class="item-cell-name"]/a/@href').extract()
        for url in urls:##problem with the for loop
            print(url)
            yield scrapy.Request("http://www.germandeli.com"+url, self.parse_product)




    def parse_product(self, response):
        #grab the url of the product image

        #grab the name, price, description and ingredients
        name_ = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        price_ = response.xpath('//*[@itemprop="price"]/text()').extract_first()
        ingredients_ = response.xpath('//*[@id="ingredients"]/text()').extract()
        description_ = response.xpath('*//div[@class="tab-pane active in"]/ul/li/text()').extract()

        image_ = response.xpath('//*[@itemprop="image"]/@src')
        image_url_ = response.xpath('//*[@itemprop="image"]/@src').extract_first()



        #yield the result and check about the splash for ingredients
        #yield scrapy.Request(item['image_url'])
        yield GermandeliMultispidersItem(name=name_, price=price_,ingredients=ingredients_,description=description_, file_urls=[image_url_]) #or yield item or return item



