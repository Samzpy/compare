import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://tescom-japan.com.tw/shop.php?uID=1&cID=5&O=0&page=1'
                

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=url,headers=headers)
        html.encoding='utf-8'
        return html.text

    def get_count(self):
        html=self.get_html(self.url)
        if html:
            parse_obj=etree.HTML(html)
            count=parse_obj.xpath('//a[@title="吹風機"]/span[@class="quantity"]/text()')[0]
            count=int(count)//12+2
            return count
    def parse_html(self):
        name_list=[]
        count=self.get_count()
        for i in range(1,count):
            url='https://tescom-japan.com.tw/shop.php?uID=1&cID=5&O=0&page={}'.format(i)
            html=self.get_html(url)
            if html:
                # print(html)
                parse_obj=etree.HTML(html)
                r_list=parse_obj.xpath('//div[@class="col-md-9 col-xs-12"]/div[@class="row"][1]/div')
                for i in r_list:
                    name=i.xpath('.//div[@class="shop-product-2"]/div[@class="info"]/a/text()')[0]
                    pn=i.xpath('.//div[@class="shop-product-2"]/div[@class="info"]/div[2]/text()')[0]
                    img_obj=i.xpath('.//div[@class="shop-product-2"]/div[@class="image"]/img/@src')[0]
                    img="https://tescom-japan.com.tw/"+img_obj
                    name='TESCOM '+name+' '+pn
                    keyword='TESCOM '+pn
                    name_list.append(['tescom','hairdryer',name,pn,keyword,img])
        # print(name_list)
        # self.write_csv(name_list)
        self.write_mysql(name_list)
        

           
    def write_csv(self,name_list):
        with open('tescom.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()