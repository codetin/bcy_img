# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    name = scrapy.Field()
    file_path = scrapy.Field()
    uid = scrapy.Field()
    nickname = scrapy.Field()
    album_id = scrapy.Field()
    cp666_album_id = scrapy.Field()
    cp666_uid  = scrapy.Field()
    pass
