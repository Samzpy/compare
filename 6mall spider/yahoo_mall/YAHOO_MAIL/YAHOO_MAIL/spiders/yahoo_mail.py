# -*- coding: utf-8 -*-
import scrapy
import pymysql
from ..items import YahooMailItem
from ..keyword_parse import Keyword_Parse
from ..mysqldb import  database

class YahooMailSpider(scrapy.Spider):
    name = 'yahoo_mail'
    allowed_domains = ['tw.mall.yahoo.com']
    urls = 'https://tw.search.mall.yahoo.com/search/mall/product?p={}'
    db=database()
    def start_requests(self):
        result=self.db.found()
        self.db.close()
        for i in result:
            url=self.urls.format(i[0])
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"com_id":i[1],"com_keyword":i[0]},
            )
        # url=self.urls.format("sadsflbjdsaf")
        # yield scrapy.Request(
        #     url=url,
        #     callback=self.parse
        # )
    def parse(self,response):
        result_list=[]
        result=response.xpath('//div[not(@class)]/ul[@class="gridList"]/li[contains(@class,"BaseGridItem__grid___2wuJ7")]')
        comId=response.meta.get("com_id")
        comKw=response.meta.get('com_keyword')
        for i in result:
            com_name=i.xpath('.//span[@class="BaseGridItem__title___2HWui"]/text()').get()
            com_price=i.xpath('.//em/text()').get().replace('$','').replace(",","")
            com_url=i.xpath('./a/@href').get()
            result_list.append((com_url,com_name,int(com_price)))

        tt=Keyword_Parse()
        #爬蟲為空
        if result_list:
            result=tt.run(result_list,comKw)
            #關鍵字排除為空
            if result:
                item=YahooMailItem()
                item['name']=result[1]
                item['com_url']=result[0]
                item['price']=str(result[2])
                item['com_id']=str(comId)
                yield item

