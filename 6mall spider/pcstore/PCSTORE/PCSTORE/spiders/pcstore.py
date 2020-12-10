# -*- coding: utf-8 -*-
import scrapy
import execjs,json,pymysql
from ..items import PcstoreItem
from ..mysqldb import  database
from ..keyword_parse import Keyword_Parse


class PcstoreSpider(scrapy.Spider):
    name = 'pcstore'
    allowed_domains = ['www.pcstore.com.tw']
    url='https://www.pcstore.com.tw/adm/api/get_search_data.php?store_k_word={}'
    db=database()

    def start_requests(self):
        result=self.db.found()
        self.db.close()
        for i in result:
            keyword = i[0]
            a=execjs.eval("encodeURIComponent('{}')".format(keyword))
            t=execjs.eval("Buffer.from('{}').toString('base64')".format(a))
            url=self.url.format(t)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"com_id":i[1],"com_keyword":i[0]}
            )

    def parse(self, response):
        result_list=[]
        com_id=response.meta.get("com_id")
        comKw=response.meta.get('com_keyword')
        html=response.body
        html=html.decode('unicode_escape')
        html=html.replace("ï»¿",'')
        t=json.loads(html,strict=False)
        for i in t['prod']:
            com_name=i['title']
            com_price=i['price'].replace(',',"")
            com_url=i['url']
            result_list.append((com_url,com_name,int(com_price)))
        tt=Keyword_Parse()
        if result_list:
            result=tt.run(result_list,comKw)
            #關鍵字排除為空
            if result:
                item=PcstoreItem()
                item['name']=result[1]
                item['com_url']=result[0]
                item['price']=str(result[2])
                item['com_id']=str(com_id)
                yield item



