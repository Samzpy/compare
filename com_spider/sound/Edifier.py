import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://shop.edifier.com.tw/product/ajaxProdList_smart.aspx?L=1609060002'

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
            li_list=parse_obj.xpath('//div[@class="row proList-img-xs-4"]/div')
            name_list=[]
            for i in li_list:
                name=i.xpath('.//h3/text()')[0].strip()
                img_obj=i.xpath('.//img/@src')[0]
                img='https://shop.edifier.com.tw/'+img_obj
                L=['edifer','sound',name,name,name,img]
                name_list.append(L)
        # self.write_csv(name_list)
        self.write_mysql(name_list)
    def write_csv(self,name_list):
        with open('edifer.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()