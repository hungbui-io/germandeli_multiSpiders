# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DropItem

from collections import defaultdict
from scrapy import signals
from scrapy.exporters import JsonItemExporter, CsvItemExporter, XmlItemExporter
import json
import codecs

class GermandeliPipeline(object):
    def process_item(self, item, spider):
        return item

# class MyExportPipeline(object):
#     def __init__(self):
#         self.files = defaultdict(list)
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         pipeline = cls()
#         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#         return pipeline
#
#     def spider_opened(self, spider):
#         csv_file = open('products.csv', 'a+b')#change the w to a
#         json_file = open('products.json', 'a+b')
#         xml_file = open('products.xml', 'a+b')
#
#         self.files[spider].append(csv_file)
#         self.files[spider].append(json_file)
#
#         self.exporters = [
#             JsonItemExporter(json_file),
#             CsvItemExporter(csv_file),
#             XmlItemExporter(xml_file)
#         ]
#
#         for exporter in self.exporters:
#             exporter.start_exporting()
#
#     def spider_closed(self, spider):
#         for exporter in self.exporters:
#             exporter.finish_exporting()
#
#         files = self.files.pop(spider)
#         for file in files:
#             file.close()
#
#     def process_item(self, item, spider):
#         for exporter in self.exporters:
#             exporter.export_item(item)
#         return item


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'a', encoding='utf-8')
        self.items_seen = set()

    def process_item(self, item, spider):
        if item['name'] in self.items_seen:
            raise DropItem("Duplicate item found: %s" % item['name'])
        else:
            self.items_seen.add(item['name'])
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
            return item

    def close_spider(self, spider):
        self.file.close()

# Add pipeline for element validation such as the item without "ingredient"

