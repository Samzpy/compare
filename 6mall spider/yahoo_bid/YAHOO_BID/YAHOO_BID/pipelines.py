# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .mysqldb import database


class YahooBidPipeline(object):
    def process_item(self, item, spider):
        # print("*"*100)
        # print(item['name'])
        # print("*"*100)
        # print(item['price'])
        # print("*"*100)
        # print(item['com_url'])
        # print("*"*100)
        # print(item['com_id'])
        # print("*"*100)
        return item

class YahooBidMysqlPipeline(object):
    db=database()

    def process_item(self,item,spider):
        self.db.insert_(item)
        self.db.close()
        return item
