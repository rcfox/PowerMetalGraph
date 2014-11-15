# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BandItem(scrapy.Item):
    band_id = scrapy.Field()
    name = scrapy.Field()
    members = scrapy.Field()
    status = scrapy.Field()
    country = scrapy.Field()
    label = scrapy.Field()
    genre = scrapy.Field()

class MemberItem(scrapy.Item):
    member_id = scrapy.Field()
    name = scrapy.Field()

class LabelItem(scrapy.Item):
    label_id = scrapy.Field()
    name = scrapy.Field()
