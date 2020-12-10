import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='http://sanlux.com.tw/s1504/sanyo_in.asp?ID1=8&ID2=6'
                

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=url,headers=headers)
        return html.text
    def parse_html(self):
        html=self.get_html(self.url)
        if html:
            # print(html)
            parse_obj=etree.HTML(html)
            name_list=[]
            r_list=parse_obj.xpath('//div[@class="inner_pro_list02"]/div')
            for i in r_list:
                url=i.xpath('.//div[@class="proImg"]/a/@href')[0]
                url='http://sanlux.com.tw/s1504/'+url
                re=self.parse_second(url)
                if re[-1] =="http://sanlux.com.tw/s1504/images/photos_ss.jpg":
                    img_obj=i.xpath('.//div[@class="proImg"]/a/img/@src')[0]
                    img='http://sanlux.com.tw/s1504/'+img_obj
                    re[-1]=img
                name_list.append(re)

            # self.write_csv(name_list)
            self.write_mysql(name_list)
    def parse_second(self,url):
        html=self.get_html(url)
        if html:
            parse_obj=etree.HTML(html)
            pn=parse_obj.xpath("//div[@class='icon']/h2/text()")[0]
            name=parse_obj.xpath("//div[@class='Instructions']/h3/text()")[0]
            img_obj=parse_obj.xpath("//div[@class='P_L']/img/@src")[0]
            img='http://sanlux.com.tw/s1504/'+img_obj
            name='SANLUX台灣三洋 '+pn+' '+name
            keyword='SANLUX 台灣三洋 ' +pn
            return ['samlux','fan',name,pn,keyword,img]
            

            

           
    def write_csv(self,name_list):
        with open('samlux.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()