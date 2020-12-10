import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql



class PHONE_Spider:
    def __init__(self):
        self.url='https://www.nakay.com.tw/product_tw.php?id=94'
                

    def get_html(self):
        ua=UserAgent()
        headers={
            'Cookie': 'PHPSESSID=0gpqn03b62jkpf0dvhqb5guqk4',
            'User-Agent':ua.random
        }
        html=requests.get(url=self.url,headers=headers,verify=False)
        #因为请求的是https 协议，所以请求禁用证书验证, 新增參數verify=False
        html.encoding='utf-8'
        return html.text
    def parse_html(self):
        html=self.get_html()
        if html:
            parse_obj=etree.HTML(html)
            name_list=[]
            r_list=parse_obj.xpath('//section[@class="itemList Bbox_in_4c"]/div/div[@class="item"]')
            for i in r_list:
                name=i.xpath('.//div[@class="itemTitle"]/a/span/text()')[0]
                pn=i.xpath('.//div[@class="itemInfo"]/span/text()')[0]
                img_obj=i.xpath('.//div[@class="itemImg"]/img/@src')[0]
                img='https://www.nakay.com.tw/'+img_obj
                name='KINYO '+name+' '+pn
                keyword='KINYO '+pn
                name_list.append(['kinyo','hairdryer',name,pn,keyword,img])
            # self.write_csv(name_list)
            self.write_mysql(name_list)
            

           
    def write_csv(self,name_list):
        with open('kinyo.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()