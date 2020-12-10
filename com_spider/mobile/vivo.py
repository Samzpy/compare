import requests
from fake_useragent import UserAgent
from lxml import etree
import csv,time
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql



class PHONE_Spider:
    def __init__(self):
        self.url='https://www.vivo.com/tw/products'
        self.gb_url='https://www.vivo.com/tw/products/param/{}'

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
            li_list=parse_obj.xpath('//div[contains(@class,"clearafter")]/a[@class="item no-flip-over"]')
            name_list=[]
            for i in li_list:
                #姓名
                name=i.xpath('.//h1/text()')[0]
                if "行動電源" == name or '無線運動耳機' in name:
                    continue
                #圖片
                img=i.xpath('.//div[@class="item-img"]/img/@data-original')
                if img:
                    img=img[0]
                else:
                    print('img有軌:',name)
                    return
                #第二層id
                id_obj=i.xpath('./@href')
                if id_obj:
                    id_obj=id_obj[0]
                    id_gb=id_obj.split('/')[-1]
                else:
                    print('擷取id有軌:',name)
                #獲取gb
                gb_url=self.gb_url.format(id_gb)
                gb=self.get_gb(gb_url)
                L=['vivo','mobile',name+" "+gb,name+" "+gb,name+" "+gb,img]
                name_list.append(L)
            # self.write_csv(name_list)
            self.write_mysql(name_list)

    def get_gb(self,gb_url):
        time.sleep(0.1)
        html=self.get_html(gb_url)
        if html:
            parse_obj=etree.HTML(html)
            gb=parse_obj.xpath('/html/body/div[3]/div[4]/div/div[3]/p/text()')
            if gb:
                gb=gb[0].split()[0]
                if gb[-1]!="B":
                    gb+="GB"
                return gb
            else:
                print("gb 出錯  ")
                
    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()

    def write_csv(self,name_list):
        with open('vivo.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
                

                


spi=PHONE_Spider()
spi.parse_html()