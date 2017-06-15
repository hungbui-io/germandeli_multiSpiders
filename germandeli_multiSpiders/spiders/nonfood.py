# -*- coding: utf-8 -*-
import scrapy
from germandeli_multiSpiders.items import GermandeliMultispidersItem
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from datetime import date


class NonfoodSpider(scrapy.Spider):
    name = "nonfood"
    allowed_domains = ["germandeli.com"]
    start_urls = ['http://germandeli.com/NonFood',
                  'http://www.germandeli.com/NonFood/Aprons_and_T-Shirts',
                  'http://www.germandeli.com/NonFood/Aprons_and_T-Shirts/German__Aprons',
                  'http://www.germandeli.com/NonFood/Buecher_Romane_Raetsel_uzw',
                  'http://www.germandeli.com/NonFood/Buecher_Romane_Raetsel_uzw/Cookbooks',
                  'http://www.germandeli.com/NonFood/Buecher_Romane_Raetsel_uzw/Cookbooks/Cookbooks_English_Language',
                  'http://www.germandeli.com/NonFood/Buecher_Romane_Raetsel_uzw/Cookbooks/Cookbooks_German_Language',
                  'http://www.germandeli.com/NonFood/Buecher_Romane_Raetsel_uzw/Kinder-Buecher',
                  'http://www.germandeli.com/NonFood/Buecher_Romane_Raetsel_uzw/Romane/Sammelbaende_2',
                  'http://www.germandeli.com/NonFood/Buecher_Romane_Raetsel_uzw/Romane/Single_Romane',
                  'http://www.germandeli.com/NonFood/Brooms_Brushes_Cloths',
                  'http://www.germandeli.com/NonFood/DetergentsCleaners',
                  'http://www.germandeli.com/NonFood/DetergentsCleaners/Gardinen_NeuCurtain_Cleansers',
                  'http://www.germandeli.com/NonFood/DetergentsCleaners/Miscellaneous_Cleansers',
                  'http://www.germandeli.com/NonFood/DetergentsCleaners/WaschmittelWeichspueler_Laundry_Helpers',
                  'http://www.germandeli.com/NonFood/Housewares',
                  'http://www.germandeli.com/NonFood/Housewares/Barware',
                  'http://www.germandeli.com/NonFood/MagazinesZeitschriften',
                  'http://www.germandeli.com/NonFood/Napkins_and_Paper_Goods', ]
    custom_settings = {'FILES_STORE': '/home/hung/Projects/germandeli_multiSpiders/output/nonfood'}

    def parse(self, response):
        urls = response.xpath('*//ul[@class="nav nav-list"]/li/h4/a/@href')
        for url in urls:
            yield scrapy.Request("http://www.germandeli.com"+str(url.extract()), self.parse_page)
            print(url.extract())

    def parse_page(self, response):
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
            print(url.extract())

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

        print(next.extract_first)


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
