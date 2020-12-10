import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://www.zushiang.com/index.php?action=pro_list02&id=31'
    def get_html(self):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random,
            'Cookie':'PHPSESSID=j8h561p3tfeiibgudkuph6kat0; lang=1'

        }
        html= requests.get(url=self.url,headers=headers)
        return html.text
    def parse_html(self):
        html=self.get_html()
        if html:
            # print(html)
            parse_obj=etree.HTML(html)
            li_list=parse_obj.xpath('//div[@class="row"]//div[contains(@class,"pro_list_thumbnail")]')
            # print(li_list)
            name_list=[]
            for i in li_list:
                pn=i.xpath('.//div[@class="caption"]/h4/text()')[0]
                pn=pn.replace('【 ','').replace(' 】','')
                name=i.xpath('.//div[@class="caption"]/p/text()')[0]+' '+pn
                img_obj=i.xpath('.//figure/a/img/@src')[0]
                img='https://www.zushiang.com/'+img_obj
                keyword='日象 '+pn
                L=['zushiang','hairdryer',name,pn,keyword,img]
                name_list.append(L)
            # self.write_csv(name_list)
            self.write_mysql(name_list)
    def write_csv(self,name_list):
        with open('zushiang.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                              

                


spi=PHONE_Spider()
spi.parse_html()