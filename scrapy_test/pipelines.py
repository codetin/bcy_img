# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os,sys

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class ScrapyTestPipeline(object):
    def process_item(self, item, spider):
        return item
    
class ImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url,meta={'item':item,'index':item['image_urls'].index(image_url)})



    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]      # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        for path in image_paths:
            move_path=dict()
            move_path['old']=os.getcwd()+'/pic/'+path
            move_path['new']=os.getcwd()+'/' +path
            print (move_path)
            os.renames(move_path['old'],move_path['new'])
        return item
    

#    def file_path(self,request,response=None,info=None):
#        item=request.meta['item'] #通过上面的meta传递过来item
#        index=request.meta['index'] #通过上面的index传递过来列表中当前下载图片的下标
#
#        #图片文件名，item['carname'][index]得到汽车名称，request.url.split('/')[-1].split('.')[-1]得到图片后缀jpg,png
#        image_guid = item['image_paths'][index]+'.jpg'
#        #图片下载目录 此处item['country']即需要前面item['country']=''.join()......,否则目录名会变成\u97e9\u56fd\u6c7d\u8f66\u6807\u5fd7\xxx.jpg
#        filename = u'full/{0}/{1}'.format('name', image_guid) 
#        return filename            
