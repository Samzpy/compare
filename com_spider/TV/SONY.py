import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://store.sony.com.tw/category/listAll/bravia'

    def get_html(self):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }

        html= requests.get(url=self.url,headers=headers)
        return html.text
    def parse_html(self):
        html=self.get_html()
        if html:
            parse_obj=etree.HTML(html)
            li_list=parse_obj.xpath('//ul[contains(@class,"solid-shadow list")]/li')
            name_list=[]
            for i in li_list:
                name=i.xpath('.//div[@class="name clamp-2"]/text()')[0]
                pn=i.xpath('.//h4[contains(@class,"display-sku")]/text()')[0]
                name='SONY '+name+' '+pn
                img_obj=i.xpath('.//div[@class="object-fit-contain product"]/img/@src')[0]
                img='https://store.sony.com.tw/'+img_obj
                keyword='SONY '+pn
                name_list.append(['sony','tv',name,pn,keyword,img])
            # self.write_csv(name_list)
            self.write_mysql(name_list)
    def write_csv(self,name_list):
        with open('sony.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()