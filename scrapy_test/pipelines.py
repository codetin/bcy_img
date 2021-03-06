# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os,sys
import pymysql

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy_test.db import db_conn
from scrapy_test.db import web_conn

class ScrapyTestPipeline(object):
    def process_item(self, item, spider):
        return item
    
class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url+'/w650',meta={'uid':item['uid'],'album_id':item['album_id']})


    #完成item下载之后进行改名
    def item_completed(self, results, item, info):
        conn = db_conn()
        cp666_conn = web_conn()
        cursor = conn.cursor()
        cursor.execute("USE bcy_scrapy")
        cursor_cp666 = cp666_conn.cursor()
        cursor_cp666.execute("USE cosplay")            
        
        image_paths = [x['path'] for ok, x in results if ok]      # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        for path in image_paths:
            sql = "INSERT INTO ct_public_upload (name,path,ext) VALUES (%s,%s,%s)"
            cursor_cp666.execute(sql,(path.split('/')[-1], '/' + path,'jpg'))
            cp666_pic = cp666_conn.insert_id()
            cursor_cp666.connection.commit()

            sql = "INSERT INTO bcy_img (auth_id,cp666_uid,album_id,cp666_album_id,cp666_pic_id,pic_path) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(item['uid'],item['cp666_uid'],item['album_id'],item['cp666_album_id'],cp666_pic, '/' + path))
            cursor.connection.commit()
  
            sql = "INSERT INTO ct_gallery_detail (gallery_id,pic,creator) VALUES (%s,%s,%s)"
            cursor_cp666.execute(sql,(item['cp666_album_id'],cp666_pic,item['cp666_uid']))
            cursor_cp666.connection.commit()
        return item

    def file_path(self,request,response=None,info=None):
        uid = request.meta['uid'] #通过上面的meta传递过来item
        album_id = request.meta['album_id'] #通过上面的index传递过来列表中当前下载图片的下标
        #图片文件名，item['carname'][index]得到汽车名称，request.url.split('/')[-1].split('.')[-1]得到图片后缀jpg,png
        image_guid = uid+'/'+album_id+'/'+request.url.split('/')[-2]
        #图片下载目录 此处item['country']即需要前面item['country']=''.join()......,否则目录名会变成\u97e9\u56fd\u6c7d\u8f66\u6807\u5fd7\xxx.jpg
        return 'Uploads/%s' % (image_guid)
