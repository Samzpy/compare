import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql



class PHONE_Spider:
    def __init__(self):
        self.url='http://www.kitchenaid-tw.com.tw/product-KFP-1333.html'
                

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
            r_list=parse_obj.xpath('//td[@align="center"]/a')
            r_list.pop()
            for i in r_list:
                pn=i.xpath('./@href')[0].split(".")[0].replace('product-','')
                img_obj=i.xpath('./img/@src')[0]
                img='http://www.kitchenaid-tw.com.tw/'+img_obj
                name='KitchenAid 食物調理機 '+pn
                keyword='KitchenAid ' +pn.replace('-','')
                name_list.append(['kitchenaid','conditioningmachine',name,pn,keyword,img])
            # self.write_csv(name_list)
            self.write_mysql(name_list)
           
           
    def write_csv(self,name_list):
        with open('kitchenaid.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
           

                


spi=PHONE_Spider()
spi.parse_html()