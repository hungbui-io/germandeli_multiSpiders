# -*- coding: utf-8 -*-
import scrapy
from germandeli_multiSpiders.items import GermandeliMultispidersItem
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from datetime import date


class SeasonalSpider(scrapy.Spider):
    name = "seasonal1"
    allowed_domains = ["germandeli.com"]
    start_urls = ['http://www.germandeli.com/Seasonal/Fasching',
                  'http://www.germandeli.com/Seasonal/Halloween',
                  'http://www.germandeli.com/Seasonal/Fathers_Day',
                  'http://www.germandeli.com/Seasonal/Mothers_Day',
                  ]
    custom_settings = {'FILES_STORE': '/home/hung/Projects/germandeli_multiSpiders/output/seasonal'}


    def parse(self, response):
        urls = response.xpath('*//h2[@class="item-cell-name"]/a/@href')
        for url in urls:
            yield SplashRequest("http://www.germandeli.com" + str(url.extract()), self.parse_product,
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
            #print(url)

        next = response.xpath('*//div[@class="pagination pagination-small pull-right"]/ul/li[3]/a/@href')
        yield SplashRequest("http://www.germandeli.com" + str(next.extract_first()), self.parse_page,
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

        #print(next)


    def parse_product(self, response):
        name_ = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        ingredients_ = response.xpath('//*[@id="ingredients"]/text()').extract()
        description_ = response.xpath('*//div[@class="tab-pane active in"]/ul/li/text()').extract()
        image_ = response.xpath('//*[@itemprop="image"]/@src')
        image_url_ = response.xpath('//*[@itemprop="image"]/@src').extract_first()
        update_on_ = date.today().isoformat()
        price_ = response.xpath('//*[@itemprop="price"]/text()').extract()
        if(1 <= len(price_)):
            price_temp = str(price_[1])
            if(1 <= len(ingredients_)):
                ingredients_temp = ingredients_[1]
                yield GermandeliMultispidersItem(name=name_, price=price_temp, ingredients=ingredients_temp, description=description_,
                                         update_on=update_on_, file_urls=[image_url_])




