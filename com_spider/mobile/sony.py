import requests
from fake_useragent import UserAgent
from lxml import etree
import csv,time
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql

class PHONE_Spider:
    def __init__(self):
        self.url='https://store.sony.com.tw/category/listAll/xperia'
        self.second_url='https://store.sony.com.tw/product/spec/{}'
        self.img='https://store.sony.com.tw/'

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url,headers=headers)
        return html.text
    def parse_html(self):
        html=self.get_html(self.url)
        if html:
            parse_obj=etree.HTML(html)
            li_list=parse_obj.xpath('//ul[contains(@class,"solid-shadow list")]/li')
            name_list=[]
            for i in li_list:
                #名稱
                name=i.xpath('.//h4/text()')[0]
                #img
                img_obj=i.xpath('.//img[@class="solid-shadow__img lazy"]/@src')[0]
                img=self.img+img_obj
                #第二層爬蟲網址
                second_obj=i.xpath('.//a[2]/@href')[0]
                second_id=second_obj.split('/')[-1]
                second_url=self.second_url.format(second_id)
                #查找GB數
                gb=self.get_gb(second_url)
                L=['sony','mobile',name+" "+gb,name+" "+gb,name+" "+gb,img]
                name_list.append(L)

            self.write_mysql(name_list)
            # self.write_csv(name_list)
    def get_gb(self,url):
        time.sleep(0.1)
        html=self.get_html(url)
        if html:
            parse_obj=etree.HTML(html)
            gb_obj=parse_obj.xpath('//div[contains(@class,cell)]//table[13][@class="normal-table"]//tr[2]/td[2]/text()')[0]
            gb=gb_obj.split()[0]
            if gb[-1] !='B':
                gb+="GB"
            return gb

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
    def write_csv(self,name_list):
        with open('sony.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
                

                


spi=PHONE_Spider()
spi.parse_html()