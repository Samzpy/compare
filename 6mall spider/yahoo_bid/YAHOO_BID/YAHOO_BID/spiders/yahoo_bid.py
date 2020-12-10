# -*- coding: utf-8 -*-
import scrapy
import pymysql
from ..items import YahooBidItem
from ..mysqldb import  database
from ..keyword_parse import Keyword_Parse


class YahooBidSpider(scrapy.Spider):
    name = 'yahoo_bid'
    allowed_domains = ['tw.bid.yahoo.com']
    urls = 'https://tw.bid.yahoo.com/search/auction/product?p={}&refine=con_new%2C-prop_3%2C-prop_2&sort=rel'
    db=database() 

    def start_requests(self):
        result=self.db.found()
        self.db.close()
        for i in result:
            # keyword = parse.quote(i[0])
            url=self.urls.format(i[0])
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"com_id":i[1],"com_keyword":i[0]},
            )

    def parse(self,response):
        result_list=[]
        com_id=response.meta.get("com_id")
        comKw=response.meta.get('com_keyword')
        result=response.xpath('//div[@class="ResultList_flexList_1NIrD"]//div[1]//ul[@class="gridList"]/li')

        for i in result:
            parse=i.xpath('.//a//span[contains(@class,"tagList")]/span/text()').get()
            if parse =="競標":
                continue
            com_name=i.xpath('.//span[@class="BaseGridItem__title___2HWui"]/text()').get()

            if com_name:
                com_name=com_name.encode('utf-8').decode('utf-8')

            #先判定是否為空在replace
            price=i.xpath('.//a//span[contains(@class,"price")]/em/text()').get()

            if price:
                com_price=price.replace('$','').replace(",","")
            else:
                continue
            com_url=i.xpath('.//a/@href').get()

            check=i.xpath('.//span[@class="multipleItems gridBottomRight"]/text()').get()
            if check:
                continue
            if com_name==None and com_price==None and com_url ==None:
                continue
            result_list.append((com_url,com_name,int(com_price)))


        tt=Keyword_Parse()
        if result_list:
            result=tt.run(result_list,comKw)
            # print(response)
            #關鍵字排除為空
            if result:
                item=YahooBidItem()
                item['name']=result[1]
                item['com_url']=result[0]
                item['price']=str(result[2])
                item['com_id']=str(com_id)
                yield item



        