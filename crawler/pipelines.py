# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import datetime

class CrawlerPipeline(object):
    def __init__(self):
        dt = datetime.datetime.now().strftime("%Y-%m-%d")
        self.file = open(dt + '.json', 'a')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
