import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql

class PHONE_Spider:
    def __init__(self):
        self.url='https://www.pinyan.com.tw/product_list.php?cid=2267&scid=2276'
                

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
            r_list=parse_obj.xpath('//div[@class="product_list"]/div/div')
            for i in r_list:
                img_obj=i.xpath('.//figure[@class="pic"]/img/@src')[0]
                img='https:'+img_obj
                url_obj=i.xpath('.//a[@class="detail"]/@href')[0]
                url_obj='https://www.pinyan.com.tw/'+url_obj
                re=self.second_parse(url_obj)
                
                name=re[0]
                pn=re[1]
                keyword=name.split()[0].replace('調理機',"")+' '+pn
                name_list.append(['blendtec','conditioningmachine',name,pn,keyword,img])
            # self.write_csv(name_list)
            self.write_mysql(name_list)
    def second_parse(self,url):
        html=self.get_html(url)   
        if html:
            parse_obj=etree.HTML(html)
            name=parse_obj.xpath('/html/body/section/div[2]/div/div/div/div[2]/div[1]/h2/text()')[1].strip().replace("+贈「食物調理機食譜」乙本","")
            pn=parse_obj.xpath('/html/body/section/div[2]/div/div/div/div[2]/div[2]/dl[1]/dd/text()')[0]

            return (name,pn)
           
    def write_csv(self,name_list):
        with open('blendtec.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()

    
                

                


spi=PHONE_Spider()
spi.parse_html()