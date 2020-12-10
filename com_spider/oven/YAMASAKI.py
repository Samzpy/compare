import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='http://www.yamasakitw.com/html/html_sk_K1.htm'
                

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
        # print(html)
        if html:
            parse_obj=etree.HTML(html)
            r_list=parse_obj.xpath('//ul[@class="P-listBox"]/li')

            for i in r_list:
                name=i.xpath('./h3/text()')[0]
                if '烤箱' not in name:
                    continue
                name=name.replace(' ','') if name[0] == " " else name
                img_obj=i.xpath('./a/img/@src')[0].replace('..','')
                pn=i.xpath('./p/text()')[0]
                name='山崎YAMAZAKI '+name+' '+pn
                keyword='山崎 '+pn
                img='http://www.yamasakitw.com'+img_obj
                name_list.append(['yamasaki','oven',name,pn,keyword,img])
            # self.write_csv(name_list)
            self.write_mysql(name_list)
           
           
    def write_csv(self,name_list):
        with open('yamasaki.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()