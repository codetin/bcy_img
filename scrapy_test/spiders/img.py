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

    def dbHandle():
        conn = pymysql.connect(
            host = "databro.cn",
            user = "root",
            passwd = "capcom",
            charset = "utf8",
            use_unicode = False
        )
        return conn

    dbObject = dbHandle()
    cursor = dbObject.cursor()
    cursor.execute("USE bcy")
    sql = "SELECT auth_url FROM today_new_come"

    try:
        cursor.execute(sql)
        cursor.connection.commit()
        today_new_come = cursor.fetchall()
        #process_sms(result[0])
    except BaseException as e:
        print("MySQL ERROR>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<error message\n")
        dbObject.rollback()

    name = 'bcy_img'
    #scrapy crawl bcy_img
    allowed_domains = ['bcy.net']

    start_urls=list()
    for i in today_new_come:
        start_urls.append("".join(i))
        #"".join将tuple单元格转换为str

    def parse(self,response):
        item = ScrapyTestItem()
        item['name']=response.css('h1.js-post-title::text').extract_first()
        urls = response.css('img.detail_std.detail_clickable::attr(src)').extract()
        item['uid'] = response.css('a.fz14.dib.maxw250.cut::attr(href)').extract_first().split('/')[-1]
        #获取uid   /u/54497 => 54497
        item['album_id'] = response.url.split('/')[-1]
        #相册id   https://bcy.net/coser/detail/10000/474890 => 474890
        item['file_path']='/' + item['uid'] +'/' + item['album_id'] +'/'
        #保存路径 /54497/474890/
        item['image_urls']=list()
        for i in urls:
            item['image_urls'].append(i[:-5])
        yield(item)
