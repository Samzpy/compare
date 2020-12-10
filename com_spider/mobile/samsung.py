import requests
from fake_useragent import UserAgent
from lxml import etree
import csv,json,time
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://searchapi.samsung.com/productfinderGlobal?type=01020000&siteCd=tw&start=0&num={}&stage=live'
        self.ua=UserAgent()
        self.headers={
            'User-Agent':self.ua.random
        }
        self.img='https://images.samsung.com/is/image/samsung/'
    def get_count(self):
        url=self.url.format(2)
        html=requests.get(url=url,headers=self.headers).json()
        count=html['response']['resultData']['common']['totalRecord']
        return count
    def get_html(self):
        count=self.get_count()
        url=self.url.format(count)
        time.sleep(0.5)
        html= requests.get(url=url,headers=self.headers).json()
        name_list=[]
        for i in range(int(count)):
            name=html['response']['resultData']['productList'][i]['fmyMarketingName']
            img=html['response']['resultData']['productList'][i]['modelList'][0]['thumbUrl']
            img=self.img+img
            try:
                optionList=html['response']['resultData']['productList'][i]["chipOptions"][1]['optionList']
            except:
                name_list.append([name+';'+'128 GB',img])
                optionList=[]
            for i in optionList:
                gb=i['optionCode'].replace(' ','')
                name_list.append(['samsung','mobile',name+' '+gb,name+' '+gb,name+' '+gb,img])

        self.write_mysql(name_list)
        # self.write_csv(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()


    def write_csv(self,name_list):
        with open('samsung.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
                

                


spi=PHONE_Spider()
# spi.parse_html()
spi.get_html()
# spi.get_count()