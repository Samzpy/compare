# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .mysqldb import database


class YahooPipeline:
    def process_item(self, item, spider):
        return item



class YahooMysqlPipeline:
    db=database()


    def process_item(self,item,spider):
        self.db.insert_(item)
        self.db.close()
        return item

   

