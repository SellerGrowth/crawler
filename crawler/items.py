# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SogouResultItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    source = scrapy.Field()

class WechatResultItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    digest = scrapy.Field()
    datetime = scrapy.Field()
    cover = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    fileid = scrapy.Field()
