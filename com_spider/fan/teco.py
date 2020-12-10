import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class Fan_Spider:
    def __init__(self):
        self.url='https://www.tecohome.com.tw/tw/ajax/Category/6/53'

                

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
            #編號
            r_list=parse_obj.xpath('//div[@class="product_txt"]/p[1]/text()')
            #姓名
            r_list2=parse_obj.xpath('//div[@class="product_txt"]/p[2]/text()')
            #圖片
            img_obj=parse_obj.xpath('//div[@class="pinner"]/a/img/@data-src')
            for pn,n,img in zip(r_list,r_list2,img_obj):
                name='TECO東元 '+ n+' '+pn
                keyword="TECO 東元 " +pn
                img='https://www.tecohome.com.tw'+img
                name_list.append(['teco','fan',name,pn,keyword,img])

            # self.write_csv(name_list)
            self.write_mysql(name_list)

           
    def write_csv(self,name_list):
        with open('teco.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=Fan_Spider()
spi.parse_html()