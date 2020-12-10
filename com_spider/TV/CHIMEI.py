import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://electronics.chimei.com.tw/display/all'

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
            parse_obj=etree.HTML(html)
            li_list=parse_obj.xpath('//*[@id="series"]/div/article/article//section[contains(@class,"series-info")]')
            name_list=[]
            for i in li_list:
                pn_obj=i.xpath('.//p[contains(@class,"model")]/text()')
                img_obj=i.xpath('.//div[@class="pic-inner"]/img/@src')
                second_url_obj=i.xpath('.//div[@class="product-box"]/div/a[@class="info"]/@href')
                for pn,img,second_url in zip(pn_obj,img_obj,second_url_obj):
                    re=self.parse_second(second_url)
                    name='CHIMEI 奇美 '+re+' '+pn
                    keyword='奇美 ' +pn

                    L=['chimei','tv',name,pn,keyword,img]
                    name_list.append(L)

            self.write_mysql(name_list)
            # self.write_csv(name_list)

    def parse_second(self,url):
        html=self.get_html(url)
        if html:
            parse_obj=etree.HTML(html)
            name_obj=parse_obj.xpath('string(//div[@class="text-inner"]/p)')
            # name_obj=parse_obj.xpath('//div[@class="text-inner"]/em/span/text()')
            return name_obj

    def write_csv(self,name_list):
        with open('chimei.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()