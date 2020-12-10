import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self,kf):
        self.kf=kf
        self.i=1
        self.url='https://kolin.com.tw/product/{}?cur_page={}'
                

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=url,headers=headers)
        return html.text
    def parse_html(self):
        name_list=[]
        while True:
            url=self.url.format(self.kf,self.i)
            html=self.get_html(url)
            # print(html)
            if html:
                parse_obj=etree.HTML(html)
                page=parse_obj.xpath('//div[contains(@class,"thumbnail")]')
                if not page:
                    break
                for i in page:     
                    pn=i.xpath('.//div[@class="caption"]/p[@class="sub-title text-center"]/text()')[0]
                    name=i.xpath('.//div[@class="caption"]/p[1]/text()')[0]
                    if name[0:2]!='歌林':
                        name='歌林'+name
                    name=name+' '+pn
                    img=i.xpath('.//img/@src')[0]
                    keyword='歌林 '+pn
                    if img[0]!='h':
                        img='https://kolin.com.tw'+img
                    name_list.append(['kolin','fan',name,pn,keyword,img])
    
            if not parse_obj.xpath('//ul[@class="pagination"]/li/a[@rel="next"]'):
                # self.write_csv(name_list)
                self.write_mysql(name_list)
                return 
            self.i+=1

           
    def write_csv(self,name_list):
        with open('kolin.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)              
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()

# spi=PHONE_Spider('kfc')
# spi.parse_html()
spi=PHONE_Spider('kf1')
spi.parse_html()



#直立風扇 kf1
#循環/大廈扇  kfc