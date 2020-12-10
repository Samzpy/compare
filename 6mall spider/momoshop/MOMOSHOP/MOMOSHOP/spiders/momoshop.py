# -*- coding: utf-8 -*-
import scrapy,pymysql
from ..items import MomoshopItem
from scrapy_splash import SplashRequest
from scrapy.http import FormRequest
from ..mysqldb import  database
import logging
import re
from urllib import parse 
from ..keyword_parse import Keyword_Parse

class MomoshopSpider(scrapy.Spider):
    name = 'momoshop'
    allowed_domains = ['www.momoshop.com.tw']
    start_url='https://www.momoshop.com.tw/search/searchShop.jsp'
   #直接導入單利模式 database
    db=database()
    def start_requests(self):
        com_id_list,queryStringList,com_keyword_list=self.db.found()
        self.db.close()

        for comId,queryString,comKw in zip(com_id_list,queryStringList,com_keyword_list):
            yield FormRequest(url=self.start_url,method='GET',meta={"com_id":comId,"com_keyword":comKw},formdata=queryString,callback=self.detail_request,dont_filter=True)
    #得到js原碼
    def detail_request(self,response):
                                   #url                    #callback                                                         #網址很像不要過濾
        comId = response.meta.get("com_id")
        comKw=response.meta.get('com_keyword')
        yield SplashRequest(response.request.url,self.deep_request,meta={'url':response.request.url,"com_id":comId,"com_keyword":comKw},endpoint='render.html',dont_filter=True)
    #得到渲染後的html
    def deep_request(self,response):

        comId = response.meta.get("com_id")
        comKw=response.meta.get('com_keyword')
        url=response.meta.get('url').replace('+',' ')

        #頁數
        # amount=response.xpath('//div[@class="pageArea topPage"]/dl/dt/span[2]/text()[2]').get().replace('/','')
        # page=int(int(amount)/30)+1
        # page=int(amount)+1
        # for page in range(1,page):
            # yield SplashRequest(url+"&curPage="+str(page),endpoint='execute',args={"lua_source":lua_script,"url":url+"&curPage="+str(page)},dont_filter=True
        # yield SplashRequest(url+"&curPage=1",endpoint='execute',args={"lua_source":lua_script,"url":url+"&curPage=1"},dont_filter=True)
        yield SplashRequest(url+"&curPage=1",dont_filter=True,meta={"com_id":comId,"com_keyword":comKw})
            
    def parse(self,response):
        result_list=[]
        comId = response.meta.get("com_id")
        comKw=response.meta.get('com_keyword')
        block_parse=response.xpath('//*[@id="BodyBase"]/div[4]/div[5]/div[2]/p/span/text()').get()
        if not block_parse:
            r_list=response.xpath('//div[@class="listArea"]/ul/li')
            for i in r_list:
                # item=MomoshopItem()
                com_name=i.xpath('./a[@class="goodsUrl"]//div[@class="prdInfoWrap"]/h3[@class="prdName"]/text()').get()
                com_price=i.xpath('./a[@class="goodsUrl"]//div[@class="prdInfoWrap"]//span[@class="price"]/b/text()').get()
                url_obj=i.xpath('./a[@class="goodsUrl"]/@href').get()
                url='https://www.momoshop.com.tw'+url_obj
                com_url=url
                result_list.append((com_url,com_name,int(com_price)))
                # yield item
            tt=Keyword_Parse()
            #爬蟲為空
            if result_list:
                result=tt.run(result_list,comKw)
                #關鍵字排除為空
                if result:
                    item=MomoshopItem()
                    item['name']=result[1]
                    item['com_url']=result[0]
                    item['price']=str(result[2])
                    item['com_id']=str(comId)
                    yield item

