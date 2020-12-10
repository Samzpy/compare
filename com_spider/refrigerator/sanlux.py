import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
#1367 
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class PHONE_Spider:
    def __init__(self):
        self.url='http://sanlux.com.tw/s1504/sanyo_in.asp?ID1=2&ID2={}'
        self.title=[1,3,6,7]

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }
        html= requests.get(url=url,headers=headers)
        return html.text
    def parse_html(self):
        name_list=[]
        for i in self.title:
            url=self.url.format(i)
            
            html=self.get_html(url)
            if html:
                parse_obj=etree.HTML(html)
                r_list=parse_obj.xpath('//div[@class="inner_pro_list02"]/div')
                for i in r_list:
                    url_obj=i.xpath('.//div[@class="proImg"]/a/@href')[0]
                    ml=i.xpath('.//div[@class="pInnerTxtSedhE-outer"]/p[1]/text()')[0].split()
                    if  ml :
                        ml=ml[0]
                        ml=ml.replace('容量：','')
                    else:
                        ml=""
                    url='http://sanlux.com.tw/s1504/'+url_obj
                    re=self.parse_second(url)
                    re[2]=re[2]+' '+ml
                    name_list.append(re)
                    # pn=i.xpath('.//h3/text()')[0]
                    # img_obg=i.xpath('.//div[@class="proImg"]/a/img/@src')[0]
                    # img='http://sanlux.com.tw/s1504/'+img_obg
                    # name_list.append(['samlux','冰箱','三洋 '+pn+';'+pn,img])

                # self.write_csv(name_list)
                self.write_mysql(name_list)
    def parse_second(self,url):
        html=self.get_html(url)
        # print(html)
        if html:
            parse_second_obj=etree.HTML(html)
            number=parse_second_obj.xpath('//div[@class="icon"]//h2/text()')[0]
            img_obj=parse_second_obj.xpath('//div[@class="P_L"]/img/@src')[0]
            img='http://sanlux.com.tw/s1504/'+img_obj
            keyword='三洋 '+number
            name=parse_second_obj.xpath('//div[@class="Instructions"]/h3/text()')[0]
            name='三洋 '+name
            return ['samlux','refrigerator',name,number,keyword,img]

            

            # name=parse_second_obj.xpath('//')

            

           
    def write_csv(self,name_list):
        with open('samlux.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
                

                


spi=PHONE_Spider()
spi.parse_html()