import  scrapy
from ..items import YahooItem
from scrapy_splash import SplashRequest
from scrapy.http import FormRequest
import logging
import re,pymysql
from ..keyword_parse import Keyword_Parse
from ..mysqldb import  database

class YahooSpider(scrapy.Spider):
    name = 'yahoo'
    start_url='https://tw.buy.yahoo.com/search/product'
    db=database()

    def start_requests(self):
        com_id_list,queryStringList,com_keyword_list=self.db.found()
        self.db.close()

        for comId,queryString,comKw in zip(com_id_list,queryStringList,com_keyword_list):
            yield FormRequest(url=self.start_url,method='GET',meta={"com_id":comId,"com_keyword":comKw},formdata=queryString,callback=self.detail_request,dont_filter=True)
    #得到js原碼
    def detail_request(self,response):
        comId=response.meta.get("com_id")
        comKw=response.meta.get('com_keyword')
                                   #url                  #callback                                                         #網址很像不要過濾
        yield SplashRequest(response.request.url,self.deep_request,meta={'url':response.request.url,"com_id":comId,"com_keyword":comKw},endpoint='render.html',dont_filter=True)
    #得到渲染後的html
    def deep_request(self,response):
        lua_script = """
        function main(splash)
        local num_scrolls = 10
        local scroll_delay = 1

        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )
        assert(splash:go(splash.args.url))
        for _ = 1, num_scrolls do
            local height = get_body_height()
            for i = 1, 10 do
                scroll_to(0, height * i/10)
                splash:wait(scroll_delay/10)
            end
        end        
        return splash:html()
        end
        """
        comId = response.meta.get("com_id")
        comKw=response.meta.get('com_keyword')
        url=response.meta.get('url')
        # amount=response.xpath('//*[@id="isoredux-root"]/div[2]/div/div[2]/div/div[1]/span/text()').get().split()[0]
        # page=int(int(amount)/60)+1
        # for page in range(1,page):
        yield SplashRequest(url+"&pg=1",endpoint='execute',args={"lua_source":lua_script,"url":url+"&pg=1"},meta={'com_id':comId,"com_keyword":comKw},dont_filter=True)
            
    def parse(self,response):
        result_list=[]
        comId=response.meta.get("com_id")
        comKw=response.meta.get('com_keyword')
        r_list=response.xpath('//*[@id="isoredux-root"]/div[2]/div/div[2]/div/div[2]/ul/li[contains(@class,"BaseGridItem__grid___2wuJ7")]')
        for i in r_list:
            item=YahooItem()
            # replenish=i.xpath('.//span[@class="BaseGridItem__statusMask___1ZrC7"]/text()').get()
            # if replenish:
            #     break
            com_name=i.xpath('.//span[@class="BaseGridItem__itemInfo___3E5Bx"]/span/text()').get()
            com_price=i.xpath('.//em/text()').get().replace("$",'').replace(",","")
            com_url=i.xpath('./a/@href').get()
            result_list.append((com_url,com_name,int(com_price)))
                #如果為空該怎麼辦呢?
        tt=Keyword_Parse()
        #爬蟲為空
        if result_list:
            result=tt.run(result_list,comKw)
            #關鍵字排除為空
            if result:
                item=YahooItem()
                item['name']=result[1]
                item['com_url']=result[0]
                item['price']=str(result[2])
                item['com_id']=str(comId)
                yield item

