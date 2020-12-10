import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='http://www.tatung.com.tw/products/index/184'
                

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=url,headers=headers)
        html.encoding='utf-8'
        return html.text
    def parse_html(self):
        name_list=[]
        html=self.get_html(self.url)
        if html:
            parse_obj=etree.HTML(html)
            r_list=parse_obj.xpath('//div[@class="pdlist-list-pdt col-xs-12 col-sm-12 col-md-12"]/div')
            for i in r_list:
                name=i.xpath('.//div[@class="row pdlist-row-box pdlist-info-box"]/h3[1]/text()')[0]
                name= name.replace('大同','') if name[0]=="大" else name
                pn=i.xpath('.//div[@class="row pdlist-row-box pdlist-info-box"]/h3[2]/text()')[0]
                img_obj=i.xpath('./a/img/@src')[0]
                img='http://www.tatung.com.tw'+img_obj
                name="大同 "+name +' '+pn
                keyword="大同 "+pn
                name_list.append(['tatung','oven',name,pn,keyword,img])
            # self.write_csv(name_list)
            self.write_mysql(name_list)
           
           
    def write_csv(self,name_list):
        with open('tatung.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()