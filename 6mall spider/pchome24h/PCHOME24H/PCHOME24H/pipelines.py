# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .mysqldb import database


class Pchome24HPipeline(object):
    def process_item(self, item, spider):

        return item

class Pchome24HMysqlPipeline(object):
    db=database()

    def process_item(self,item,spider):
        self.db.insert_(item)
        self.db.close()
        return item

