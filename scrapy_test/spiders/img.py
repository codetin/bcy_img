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
    sql = "SELECT auth_url FROM album_list limit 10"

    try:
        cursor.execute(sql)
        cursor.connection.commit()
        today_new_come = cursor.fetchall()
    except BaseException as e:
        print("MySQL ERROR>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<error message\n")
        dbObject.rollback()

    name = 'bcy_img'
    allowed_domains = ['bcy.net']

    start_urls=list()
    for i in today_new_come:
        start_urls.append("".join(i))
        #"".join将tuple单元格转换为str

    def parse(self,response):
        conn = pymysql.connect(
            host = "databro.cn",
            user = "root",
            passwd = "capcom",
            charset = "utf8",
            use_unicode = False
        )

        cp666_conn = pymysql.connect(
            host = "databro.cn",
            user = "root",
            passwd = "capcom",
            charset = "utf8",
            use_unicode = False
        )
        
        item = ScrapyTestItem()
        item['name']=response.css('h1.js-post-title::text').extract_first()
        urls = response.css('img.detail_std.detail_clickable::attr(src)').extract()
        item['uid'] = response.css('a.fz14.dib.maxw250.cut::attr(href)').extract_first().split('/')[-1]
        #获取uid   /u/54497 => 54497
        item['album_id'] = response.url.split('/')[-1]
        #相册id   https://bcy.net/coser/detail/10000/474890 => 474890

        item['file_path']='/' + item['uid'] +'/' + item['album_id'] +'/'
        #保存路径 /54497/474890/

        cursor_cp666 = cp666_conn.cursor()
        cursor_cp666.execute("USE cosplay")            
        
        cursor = conn.cursor()
        cursor.execute("USE bcy")        

        #判断BCY用户是否存在,如不存在则在CP666上新建帐号,使用BCY的用户ID作为CP666的用户名
        try:
            sql = "select id from ct_user where username = %s"
            cursor_cp666.execute(sql,(item['uid']))
            result = cursor_cp666.fetchone()
        except BaseException as e:
            print("mysql daily error>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<error message")
            cp666_conn.rollback()
        if result is not None:
            item['cp666_uid'] = int(result[0])
        if result is None:
            sql = "insert into ct_user (username,password) VALUES (%s,%s)"
            cursor_cp666.execute(sql,(item['uid'],'505131577c0f9f236fcffc72d5e1b1d0'))
            item['cp666_uid'] = cp666_conn.insert_id()
            cursor_cp666.connection.commit()
        
        
        #新建CP666相册,获取相册ID,然后建立与BCY相册的对应关系
 
        try:
            sql = "INSERT INTO ct_gallery (creator,title) VALUES (%s,%s)"
            cursor_cp666.execute(sql,(item['cp666_uid'],item['name']))
            item['cp666_album_id'] = cp666_conn.insert_id()
            cursor_cp666.connection.commit()
        except BaseException as e:
            print("mysql daily error>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<error message")
            cp666_conn.rollback()
        
        try:
            sql = "INSERT INTO bcy_album (bcy_album_id,cp666_album_id) VALUES (%s,%s)"
            cursor.execute(sql,(item['album_id'],item['cp666_album_id']))
            cursor.connection.commit()
        except BaseException as e:
            print("mysql daily error>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<error message")
            conn.rollback()

        
        
        #插入CP666的用户相册表
        

        item['image_urls']=list()
        for i in urls:
            item['image_urls'].append(i[:-5])
            #item['image_urls'].append(i)
        yield(item)
