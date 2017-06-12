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
        item = GermandeliMultispidersItem()
        # image = response.css("").xpath("@src")
        # image_url = image.extract_first()

        #grab the name, price, description and ingredients
        item['name'] = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        item['price'] = response.xpath('//*[@itemprop="price"]/text()').extract_first()
        item['ingredients'] = response.xpath('//*[@id="ingredients"]/text()').extract()
        item['description'] = response.xpath('*//div[@class="tab-pane active in"]/ul/li/text()').extract()
        print(item['name'] )
        print(item['price'])
        print(item['ingredients'])


        #yield the result and check about the splash for ingredients
        return item



