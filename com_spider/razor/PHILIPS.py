import requests
from fake_useragent import UserAgent
from lxml import etree
import csv,time
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://www.philips.com.tw/c-m-pe/face-shavers/series-shavers/latest#filters=SERIES_SHAVERS_SU&page={}'

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=url,headers=headers)
        return html.text

    def get_count(self):
        url=self.url.format(0)
        html=self.get_html(url)
        if html:
            parse_obj=etree.HTML(html)
            total=parse_obj.xpath('/html/body/div[3]/div[2]/div[1]/div/div/h2/span/span/text()')[0]
            count=int(total)//12+1
            time.sleep(0.1)
            return count
    def parse_html(self):
        name_list=[]
        for i in range(self.get_count()):
            url=self.url.format(i)
            html=self.get_html(url)
            if html:
                parse_obj=etree.HTML(html)
                li_list=parse_obj.xpath('/html/body/div[3]/div[2]/div[2]/div/div/div[2]/div[3]/div/div/ul/li')
                for i in li_list:
                    name=i.xpath('.//span[@class="p-heading-light"]/text()')[0].strip()
                    pn=i.xpath('.//p[@class="p-pc05v2__card-ctn p-body-copy-03 p-heading-light"]/text()')[0].strip().split("/")[0]
                    name='Philips飛利浦' +name +' '+pn
                    keyword='Philips飛利浦 '+pn
                    img=i.xpath('.//picture[@class="p-picture p-product-picture"]/img/@src')[0]
                    name_list.append(['philips','razor',name,pn,keyword,img])

        # self.write_csv(name_list)
        self.write_mysql(name_list)
    def write_csv(self,name_list):
        with open('philps.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()
# spi.get_count()