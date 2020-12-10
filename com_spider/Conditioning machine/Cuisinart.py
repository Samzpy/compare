import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='http://www.cuisinart.com.tw/product.php?tb=1&lang=tw&id=2'
                

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
            r_list=parse_obj.xpath('//td[@class="t10"]/div//td[@width="331"]/table[@width="331"]/tr/td[2]//a[2]/@href')
            for i in r_list:
                url='http://www.cuisinart.com.tw/'+i
                re=self.parse_second(url)
                name_list.append(re)
            #     img=i.xpath('./td[1]//a/img/@src')[0]
            #     pn=i.xpath("string(./td[2]//a)")
            #     pn=pn.split()[0]
            #     name='Cuisinart '+pn +"調理機"
            #     keyword='Cuisinart '+pn
            #     name_list.append(['cuisinart','調理機',name,pn,img])
                # print(name_list)
            # self.write_csv(name_list)
            self.write_mysql(name_list)
    def parse_second(self,url):
        html=self.get_html(url)
        if html:
            parse_obj=etree.HTML(html)
            img=parse_obj.xpath('//*[@id="showmainimg"]/@src')[0]
            name=parse_obj.xpath('//td[@class="t19"]/text()')[0]
            pn=name.split()[0]
            keyword='Cuisinart '+pn
            return ['cuisinart','conditioningmachine','Cuisinart '+name,pn,keyword,img]

           
           
    def write_csv(self,name_list):
        with open('cuisinart.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()

                

                


spi=PHONE_Spider()
spi.parse_html()