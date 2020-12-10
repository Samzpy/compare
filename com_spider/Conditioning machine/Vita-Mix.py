import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://www.diet-u.com.tw/stm_works_category/conditioning-machine/'
                

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
            r_list=parse_obj.xpath('//div[@class="posts_list with_sidebar"]/ul/li')
            for i in r_list:
                re=i.xpath('.//h4/text()')[0]
                re=re.split()
                name=re[0]+' '+re[1]+' '+re[2]
                pn=re[1]
                keword=re[0] +' '+re[1]

                img=i.xpath('.//div[@class="post_thumbnail"]/img/@src')[0]
                name_list.append(['vitamix','conditioningmachine',name,pn,keword,img])
            # self.write_csv(name_list)
            self.write_mysql(name_list)
           
           
    def write_csv(self,name_list):
        with open('vita-mix.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()

                

                


spi=PHONE_Spider()
spi.parse_html()