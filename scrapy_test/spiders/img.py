# -*- coding: utf-8 -*-
#encoding=utf-8
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import scrapy
import datetime
from scrapy_test.items import ScrapyTestItem
import pymysql

class scrapy_test(scrapy.Spider):
    name = 'scrapy_test'
    allowed_domains = ['bcy.net']
    now = datetime.datetime.now()
    start_urls = ['https://bcy.net/coser/detail/86897/2076989']

    def parse(self,response):
        item = ScrapyTestItem()
        item['name']=response.css('h1.js-post-title::text').extract_first()
        urls = response.css('img.detail_std.detail_clickable::attr(src)').extract()

        item['filepath']='test'
        item['image_urls']=list()
        for i in urls:
            item['image_urls'].append(i[:-5])

        yield(item)
