import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://www.panasonic.com/tw/consumer/beauty/mens-shaver.html?page={}'
                

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=url,headers=headers)
        return html.text
    def parse_html(self):
        url=self.url.format(1)
        html=self.get_html(url)
        if html:
            parse_obj=etree.HTML(html)
            page=parse_obj.xpath('//*[@id="categorybrowse-filterbar"]/div/div/div/div[1]/div/h3/span[2]/text()')[0]
            count=int(page)//30+1
            name_list=[]
            for i in range(1,count+1):
                html=self.url.format(i)
                re=self.second_parse(html)
                name_list+=re
            # self.write_csv(name_list)
            self.write_mysql(name_list)


    def second_parse(self,html):
        html=self.get_html(html)
        parse_obj=etree.HTML(html)
        name_list=[]
        r_list=parse_obj.xpath('//*[contains(@id,"categorybrowse-results")]/div[2]/div/div[2]/div/div')
        for i in r_list:
            img_obj=i.xpath('.//div[@class="common-productbox-product__image__box"]/img/@src')[0]
            img='https://www.panasonic.com'+img_obj
            pn=i.xpath('string(.//span[@class="num"])')
            name="Panasonic國際牌 "+pn +'括弧刀'
            keyword='Panasonic國際牌 '+pn
            name_list.append(['panasonic','razor',name,pn,keyword,img])
        else:
            return name_list

           
    def write_csv(self,name_list):
        with open('panasonic.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()