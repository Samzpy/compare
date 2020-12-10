import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql


class Sound_Spider:
    def __init__(self):
        self.url='https://www.bose.tw/speakers.search.html?spUrl=?count=12;i=1;page={};q1=TW;q2=speakers;q3=zh;q32=~2Fcontent~2Fconsumer_electronics~2Fb2c_catalog~2Fworldwide~2Fwebsites~2Fzh_tw~2F;q4=Product;q5=Product;q6=10001dcfc0d9aa319e93714459412b81;sp_cs=UTF-8;x1=country;x2=category1;x3=language;x32=siteRootPagePath;x4=contentType;x5=productType;x6=space&path=/content/consumer_electronics/b2c_catalog/worldwide/websites/zh_tw/index/shop_all/speakers/speakers/jcr:content/parsys/productdrawer_aa4e/productDrawerResultSet&tab=Product&facets=,nestedFeatures'

    def get_html(self,url):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }

        html= requests.get(url=url,headers=headers)
        return html
    def get_count(self):
        url='https://www.bose.tw/zh_tw/shop_all/speakers/speakers.html'
        html=self.get_html(url).text
        if html:
            parse_obj=etree.HTML(html)
            count=parse_obj.xpath('/html/body/main/section/div/div[2]/div/div/div[2]/div/h3/span/text()')[0]
        return count


    def parse_html(self):
        count=self.get_count()
        page=int(count)//12 +1
        name_list=[]
        for i in range(1,page+1):
            url=self.url.format(i)
            html=self.get_html(url).json()['htmlResult']
            parse_obj=etree.HTML(html)
            img=parse_obj.xpath('//div[@class="bose-productTile2020__imageWrapper light-grey"]//img/@data-src')
            count=parse_obj.xpath('//p[@class="bose-title__link js-productTitle__link"]/text()')

            for i in count:
                if i.strip()=="":
                    count.remove(i) 
            for count,img in zip(count,img):             
                name=count.strip()
                if "揚聲器" not in name:
                    continue
                L=["bose","sound","BOSE音響 "+name,name,name,'https:'+img]
                name_list.append(L)
        # self.write_csv(name_list)
        self.write_mysql(name_list)
    def write_csv(self,name_list):
        with open('bose.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)

    def write_mysql(self,name_list):
        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()


spi=Sound_Spider()
spi.parse_html()


