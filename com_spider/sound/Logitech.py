import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://www.logitech.com/zh-tw/speakers-audio'

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
            li_list=parse_obj.xpath('//div[contains(@class,"row no-gutter uncategorized unsorted product-grid")]//div[@class="inner"]')
            name_list=[]
            for i in li_list:
                name=i.xpath('string(.//span[@class="product-name"])').strip()
                img_obj=i.xpath('.//a/img/@src')[0]
                img='https://www.logitech.com'+img_obj
                L=['logitech','sound','LOGITECH音響 '+name,name,'LOGITECH '+name,img]
                name_list.append(L)
            self.write_mysql(name_list)
            # self.write_csv(name_list)
    def write_csv(self,name_list):
        with open('logitech.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()