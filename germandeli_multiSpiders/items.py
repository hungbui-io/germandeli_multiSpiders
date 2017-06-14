# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GermandeliMultispidersItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    ingredients = scrapy.Field()
    files = scrapy.Field()
    file_urls = scrapy.Field()
    update_on = scrapy.Field()
    #index = scrapy.Field()
