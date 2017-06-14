# -*- coding: utf-8 -*-
import scrapy
from germandeli_multiSpiders.items import GermandeliMultispidersItem
from scrapy.selector import Selector
from scrapy_splash import SplashRequest


class GroceriesSpider(scrapy.Spider):
    name = "groceries"
    allowed_domains = ["germandeli.com"]
    start_urls = ['http://germandeli.com/Groceries']
    custom_settings = {'FILES_STORE': '/home/hung/Projects/germandeli_multiSpiders/output/groceries'}

    def parse(self, response):
        urls = response.xpath('*//div[@class="category-cell-name"]/a/@href').extract()
        for url in urls:
            if url is not None:
                yield scrapy.Request("http://www.germandeli.com/"+url, self.parse_page)
                print(url)

    def parse_page(self, response):
        urls = response.xpath('*//h2[@class="item-cell-name"]/a/@href').extract()
        for url in urls:
            if url is not None:
                yield SplashRequest("http://www.germandeli.com" + url, self.parse_product,
                                    args={
                                        # optional; parameters passed to Splash HTTP API
                                        'wait': 0.5,
                                        'timeout': 10,

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
        if next is not None:
            yield scrapy.Request("http://www.germandeli.com" + next, self.parse_page, meta={
            'splash': {
            'args': {
            # set rendering arguments here
                'html': 1,
                'png': 1,
                'wait': 0.5,
                'timeout': 10,
            # 'url' is prefilled from request url
            # 'http_method' is set to 'POST' for POST requests
            # 'body' is set to request body for POST requests
                     },

            # optional parameters
            'endpoint': 'render.html',  # optional; default is render.json
            'splash_url': '<url>',  # optional; overrides SPLASH_URL
            'slot_policy': scrapy_splash.SlotPolicy.PER_DOMAIN,
            # 'splash_headers': {},  # optional; a dict with headers sent to Splash
            # 'dont_process_response': True,  # optional, default is False
            # 'dont_send_headers': True,  # optional, default is False
            # 'magic_response': False,  # optional, default is True
               }
             })
            #

        print(next)


    def parse_product(self, response):
        name_ = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        price_ = response.xpath('//*[@itemprop="price"]/text()').extract_first()
        ingredients_ = response.xpath('//*[@id="ingredients"]/text()').extract()
        description_ = response.xpath('*//div[@class="tab-pane active in"]/ul/li/text()').extract()

        image_ = response.xpath('//*[@itemprop="image"]/@src')
        image_url_ = response.xpath('//*[@itemprop="image"]/@src').extract_first()

        yield GermandeliMultispidersItem(name=name_, price=price_,ingredients=ingredients_,description=description_, file_urls=[image_url_])



