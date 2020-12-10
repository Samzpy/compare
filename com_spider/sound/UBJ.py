import requests
from fake_useragent import UserAgent
from lxml import etree
import csv,time
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://www.jbl.com.tw/loudspeakers?start={}'

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }

        html= requests.get(url=url,headers=headers)
        return html.text
    def parse_html(self):
        name_list=[]
        for i in range(0,100,12):
            url=self.url.format(i)
            html=self.get_html(url)
            if html:
                parse_obj=etree.HTML(html)
                li_list=parse_obj.xpath('//*[@id="search-result-items"]/div')
                img=parse_obj.xpath('//a[@class="thumb-link"]/img/@data-src')
                if not li_list:
                    break
                for img,i in zip(img,li_list):
                    re=i.xpath('.//a[@class="productname-link"]/text()')[0].strip().replace('®','')
                    name=i.xpath('.//a[@class="product-description"]/text()')[0].strip()
                    name=re+' '+name
                    name=name.replace('"',"")
                    L=['jbl','sound',name,re,re,img]
                    name_list.append(L)
                time.sleep(0.5)
        # self.write_csv(name_list)
        self.write_mysql(name_list)
    def write_csv(self,name_list):
        with open('ubj.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

spi=PHONE_Spider()
spi.parse_html()

