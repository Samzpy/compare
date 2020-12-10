import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='https://www.lg.com/tw/mkt/ajax/category/retrieveCategoryProductList'
        self.data={
            'categoryId': 'CT20224042',
            'modelStatusCode': 'ACTIVE',
            'bizType': 'B2C',
            'viewAll': 'Y',
            'filterFlag': 'Y',
            'page': 'viewAll',
            'pdfDownloadFile': 'pdf下載文件',
            'productFicheDownload': 'component-productFicheDownload'
        }

    def get_html(self):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }

        html= requests.post(url=self.url,headers=headers,data=self.data)
        html.encoding='UTF-8'
        return html.json()
    def parse_html(self):
        html=self.get_html()
        name_list=[]
        if html:
            model_list=html['data'][0]["productList"]
            for i in range(len(model_list)):
                name=model_list[i]['userFriendlyName']
                if '冰箱' not in name:
                    continue
                pn=model_list[i]['modelName']
                img_obj=model_list[i]['mediumImageAddr']
                img='https://www.lg.com'+img_obj
                name='LG '+name
                keyword='LG '+pn
                L=['lg','refrigerator',name,pn,keyword,img]
                name_list.append(L)

            # self.write_csv(name_list)
            self.write_mysql(name_list)
            

           
    def write_csv(self,name_list):
        with open('lg.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

spi=PHONE_Spider()
spi.parse_html()