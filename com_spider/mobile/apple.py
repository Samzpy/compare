import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import datetime
import sys,os,re
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql




class PHONE_Spider:
    def __init__(self):
        self.url='https://support.apple.com/zh-tw/HT201296'
        self.i=4
        self.now_year=int(datetime.datetime.now().year)-3
    def get_html(self):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }

        html= requests.get(url=self.url,headers=headers)
        return html.text
    def parse_html(self):
        html=self.get_html()
        total_list=[]
        name_list=[] #還差img網址
        L=[]
        if html:
            parse_obj=etree.HTML(html)
            while True:
                name=parse_obj.xpath('//div[@id="sections"]/div[{}]/h2/text()'.format(self.i))
                if name:
                    name=name[0]
                modify=re.findall(r'(（.*?）)',name)
                if modify:
                    name=name.replace(modify[0],'')
                li_list=parse_obj.xpath('//div[@id="sections"]/div[{}]/div/p[1]/text()'.format(self.i))
                L=[]
                for i in li_list:
                    i=i.strip()
                    try:
                        result=i.split('：')[1]
                    except:
                        pass
                    L.append(result)

                total_list.append(L)
                years=total_list[-1][0]
                # pn=total_list[-1][3].split('、')[0].split("（")[0]
                GB=total_list[-1][1].split('、')
                # 判斷
                if int(years) < self.now_year :
                    break
                else:
                    # print(name)
                    self.i-=1
                    re_img=parse_obj.xpath('//*[@id="sections"]/div[{}]//img/@src'.format(self.i))[0]
                    img='https://support.apple.com/'+re_img

                    # 總結
                    for gb in GB:
                        if gb[-1] != 'B':
                            gb+='GB'
                        #品牌,分類,商品名稱,編碼,關鍵字索引,圖片
                        re_name=['apple','mobile',name+' '+gb,name+' '+gb,name+' '+gb,img]
                        name_list.append(re_name)
                    self.i+=4
            # self.write_csv(name_list)
            self.write_mysql(name_list)
    
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()


    def write_csv(self,name_list):
        with open('apple.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
                

                


spi=PHONE_Spider()
spi.parse_html()