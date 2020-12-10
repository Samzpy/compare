import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://www.heran.com.tw/product-category/kitchen/electric-stove/'
                

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=url,headers=headers)
        return html.text
    def parse_html(self):
        name_list=[]
        html=self.get_html(self.url)
        if html:
            parse_obj=etree.HTML(html)
            r_list=parse_obj.xpath('//div[@class="products row row-small large-columns-4 medium-columns-3 small-columns-2"]/div')

            for i in r_list:
                re=i.xpath('.//div[@class="title-wrapper"]//p[@class="name product-title"]/a/text()')[0]
                name=re.split()[1]
                pn=re.split()[0]
                img=i.xpath('.//div[@class="box-image"]/div[@class="image-fade_in_back"]/a/img/@src')[0]
                name='禾聯 '+name+' '+pn
                keyword="禾聯 "+pn
                name_list.append(['heran','oven',name,pn,keyword,img])
            # self.write_csv(name_list)
            self.write_mysql(name_list)
           
           
    def write_csv(self,name_list):
        with open('heran.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()