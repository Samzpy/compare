import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import json
import re
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql

class PHONE_Spider:
    def __init__(self):
        self.url='https://global.joyoung.com/zh-tw/product/category/8'
                

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
            r_list=parse_obj.xpath('.//script[@type="text/javascript"][1]/text()')[0]
            name=re.findall('.*?"infos": { \s*"p_name": "(.*?)",',r_list)
            pn=re.findall('.*?"p_area": .*?\s*"p_number": "(.*?)",',r_list)
            img_obj=re.findall('"p_img_url": "(.*?)"',r_list)
            for n,p,i in zip(name,pn,img_obj):
                if '理機' not in n:
                    continue
                final_name = '九陽 '+ n +' '+p
                final_pn=p   
                final_keyword='九陽 '+p
                final_img ="https://global.joyoung.com"+i
                L=['joyoung','conditioningmachine',final_name,final_pn,final_keyword,final_img]
                name_list.append(L)

            # self.write_csv(name_list)
            self.write_mysql(name_list)

           
    def write_csv(self,name_list):
        with open('joyoung.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()

                

                


spi=PHONE_Spider()
spi.parse_html()