import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql

#1367 

class PHONE_Spider:
    def __init__(self):
        self.url='https://tw.sharp/products/refrigerator?page={}'
        self.i=0
    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=url,headers=headers)
        if html.status_code!=200:
            return None
        
        return html.text
    def parse_html(self):
        name_list=[]
        while True:
            url=self.url.format(self.i)
            html=self.get_html(url)
            if html:
                parse_obj=etree.HTML(html)
                r_list=parse_obj.xpath('//div[@class="list-row"]//div[@class="row"]/div')
                for i in r_list:
                    second_url_obj=i.xpath('.//div[@class="pic-wrapper"]/a/@href')[0]
                    second_url='https://tw.sharp/'+second_url_obj
                    re=self.second_parse(second_url)
                    if not re:
                        continue
                    pn=i.xpath('.//div[@class="name-wrapper"]/span/text()')[0]
                    name_obj=re[0]
                    img=re[1]
                    ml=i.xpath('.//div[@class="type-wrapper"]/a/text()')[0]
                    name='SHARP ' +name_obj+' '+ml +' ' +pn
                    keyword="SHARP "+pn
                    name_list.append(['sharp','refrigerator',name,pn,keyword,img])

                if not parse_obj.xpath('//li[@class="next"]/a[@rel="next"]'):
                    # self.write_csv(name_list)
                    self.write_mysql(name_list)
                    return

                self.i+=1
    def second_parse(self,url):
        html=self.get_html(url)
        if html:
            second_parse_obj=etree.HTML(html)
            img_obj=second_parse_obj.xpath('//div[@id="commerce-product-images-large"]/div[1]/img/@src')[0]
            name=second_parse_obj.xpath('//div[@id="product-details-mobile-menu"]/div[2]/text()')[0]
            img='https://tw.sharp/'+img_obj
            return name,img


           
    def write_csv(self,name_list):
        with open('sharp.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()