# -*- coding: utf-8 -*-
import scrapy
import pymysql,json
from ..items import Pchome24HItem
from urllib import parse
from fake_useragent import UserAgent
from ..mysqldb import  database
from ..keyword_parse import Keyword_Parse

class Pchome24hSpider(scrapy.Spider):
    name = 'pchome24h'
    allowed_domains = ['24h.pchome.com.tw']
    urls = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={}&page=1&sort=sale/dc'
    useragent=UserAgent()
    db=database()
    def start_requests(self):
        headers={'User-Agent':self.useragent.random}
        result=self.db.found()
        self.db.close()
        for i in result:
            # keyword = parse.quote(i[0])
            url=self.urls.format(i[0])
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"com_id":i[1],"com_keyword":i[0]},
                headers=headers
            )
    def parse(self, response):
        result_list=[]
        com_id=response.meta.get("com_id")
        comKw=response.meta.get('com_keyword')

        html=response.text
        html=json.loads(html)     
        for i in html['prods']:
            com_name=i['name']
            com_price=i['price']
            com_url='https://24h.pchome.com.tw/books/prod/'+i['Id']
            result_list.append((com_url,com_name,int(com_price)))
        tt=Keyword_Parse()
        #爬蟲為空
        if result_list:
            result=tt.run(result_list,comKw)
            #關鍵字排除為空
            if result:
                item=Pchome24HItem()
                item['name']=result[1]
                item['com_url']=result[0]
                item['price']=str(result[2])
                item['com_id']=str(com_id)
                yield item


