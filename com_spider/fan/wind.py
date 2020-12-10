import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='http://www.supafine.com.tw/product.php?level1=1&level2=67&page={}'
        self.i=1
                

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
        while True:
            url=self.url.format(self.i)
            html=self.get_html(url)
            if html:
                parse_obj=etree.HTML(html)
                #編號
                r_list=parse_obj.xpath('//td[@valign="bottom"]//td/span[2]/text()')
                #名稱
                r_list2=parse_obj.xpath('//td[@valign="bottom"]//td/span[2]/a/text()')
                #圖片
                img_obj=parse_obj.xpath('//td[@class="product_run"]/a/img/@src')
                for pn,n,img in zip(r_list,r_list2,img_obj):
                    name='勳風 '+ n +' '+pn
                    keyword='勳風 '+pn
                    img='http://www.supafine.com.tw/'+img
                    name_list.append(['wind','fan',name,pn,keyword,img])
            self.i+=1
            if not parse_obj.xpath('//a[@title="Next"]/text()'):
                # self.write_csv(name_list)
                self.write_mysql(name_list)
                break
           
    def write_csv(self,name_list):
        with open('wind.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()