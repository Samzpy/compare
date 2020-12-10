import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://www.panasonic.com/tw/consumer/air-conditioner/electric-fan.html'
                

    def get_html(self):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=self.url,headers=headers)
        html.encoding='urf-8'
        return html.text
    def parse_html(self):
        html=self.get_html()
        if html:
            # print(html)
            parse_obj=etree.HTML(html)
            name_list=[]
            r_list=parse_obj.xpath('//*[contains(@id,"categorybrowse-results")]/div[2]/div/div[2]/div/div')
            for i in r_list:
                pn=i.xpath('.//span[@class="num"]/text()')[0]
                name=i.xpath('.//span[@class="copy"]/text()')[0]
                img_obj=i.xpath('.//div[@class="common-productbox-product__image__box"]/img/@src')[0]
                img="https://www.panasonic.com/"+img_obj
                keyword='PANASONIC '+pn
                name='Panasonic '+name+'電扇 '+pn
                name_list.append(['panasonic','fan',name,pn,keyword,img])
            # self.write_csv(name_list)
            self.write_mysql(name_list)
            

           
    def write_csv(self,name_list):
        with open('panasonic.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()