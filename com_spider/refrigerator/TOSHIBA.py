import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='http://www.grainew.com.tw/p1_product1.asp?cid=3'
        self.target_url="http://www.grainew.com.tw/"

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=url,headers=headers)
        return html.text
    def get_url(self):
        html=self.get_html(self.url)
        parse_obj=etree.HTML(html)
        url=parse_obj.xpath('//ul[@class="product_list"]/li/a/@href')
        return url

    def parse_html(self):
        _list=[]
        for i in self.get_url():
            url=self.target_url+i            
            html=self.get_html(url)
            if html:
                parse_obj=etree.HTML(html)
                r_list=parse_obj.xpath('//div[@class="txt"]')
                img_list=parse_obj.xpath('//div[@class="img"]/a')
                for i,o in zip(r_list,img_list):
                    pn=i.xpath('.//a[1]/text()')[0]
                    name=i.xpath('.//a[1]/strong/text()')[0]
                    img_obj=o.xpath('./img/@src')[0]
                    name='東芝 '+name+' ' +pn
                    img='http://www.grainew.com.tw/'+img_obj
                    if "系列" in pn:                        
                        url2=parse_obj.xpath('//div[@class="txt"]/a[1]/@href')[0]
                        html=self.get_html(self.target_url+url2)
                        gr_List=self.get_second(html)
                        for a in gr_List:
                            number=a[1].split()[0]
                            name=a[0]+' '+a[1].split()[1] +number
                            keyword='TOSHIBA '+number
                            _list.append(['toshiba','refrigerator',name,number,keyword,img])
                        continue

                    keyword="TOSHIBA "+pn
                    _list.append(['toshiba','refrigerator',name,pn,keyword,img])
                                 
        # self.write_csv(_list)
        self.write_mysql(_list)

    def get_second(self,html):
        L=[]
        if html:
            parse_obj=etree.HTML(html)
            r_list=parse_obj.xpath('//div[@class="prd_right"]/p/strong/text()')
            name=parse_obj.xpath('//div[@class="prd_right"]/h1/text()')[0]

            for i in r_list:
                L.append([name,i.strip()])
            return L

           
    def write_csv(self,name_list):
        with open('toshiba.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()