# -*- coding: utf-8 -*-
import scrapy
from germandeli_multiSpiders.items import GermandeliMultispidersItem
from scrapy.selector import Selector
from scrapy_splash import SplashRequest


class MeatsSpider(scrapy.Spider):
    name = "meats"
    allowed_domains = ["germandeli.com"]
    start_urls = ['http://germandeli.com/Meats']

    def parse(self, response):
        urls = response.xpath('*//div[@class="category-cell-name"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request("http://www.germandeli.com/"+url, self.parse_page)
            print(url)

    def parse_page(self, response):
        urls = response.xpath('*//h2[@class="item-cell-name"]/a/@href').extract()
        for url in urls:
            yield SplashRequest("http://germandeli.com" + url, self.parse_product,
                                args={
                                    # optional; parameters passed to Splash HTTP API
                                    'wait': 0.5,
                                    # 'timeout': 10,

                                    # 'url' is prefilled from request url
                                    # 'http_method' is set to 'POST' for POST requests
                                    # 'body' is set to request body for POST requests
                                },
                                endpoint='render.html',  # optional; default is render.html
                                # splash_url='<url>',  # optional; overrides SPLASH_URL
                                # slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                )
            print(url)

        next = response.xpath('*//div[@class="pagination pagination-small pull-right"]/ul/li[3]/a/@href').extract_first()
        yield SplashRequest("http://germandeli.com" + next, self.parse_page,
                            args={
                                # optional; parameters passed to Splash HTTP API
                                'wait': 0.5,
                                # 'timeout': 10,

                                # 'url' is prefilled from request url
                                # 'http_method' is set to 'POST' for POST requests
                                # 'body' is set to request body for POST requests
                            },
                            endpoint='render.html',  # optional; default is render.html
                            # splash_url='<url>',  # optional; overrides SPLASH_URL
                            # slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                            )
        print(next)


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
        yield SplashRequest(GermandeliMultispidersItem(name=name_, price=price_,ingredients=ingredients_,description=description_, file_urls=[image_url_]),
                            args={
                                # optional; parameters passed to Splash HTTP API
                                'wait': 0.5,
                                # 'timeout': 10,

                                # 'url' is prefilled from request url
                                # 'http_method' is set to 'POST' for POST requests
                                # 'body' is set to request body for POST requests
                            },
                            endpoint='render.html',  # optional; default is render.html
                            # splash_url='<url>',  # optional; overrides SPLASH_URL
                            # slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                            )




