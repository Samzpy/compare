
import requests
from fake_useragent import UserAgent
from xml import etree
import os 



class PHONE_Spider:
    def __init__(self):
        self.url='https://www.samsung.com/tw/smartphones/all-smartphones/'

    def get_html(self):
        ua=UserAgent()
        headers={
            'User-Agent':ua.random
        }

        html= requests.get(url=self.url,headers=headers)
        # html.encoding='cp950'
       
        # a=html.content
        # a=a.decode("utf-8","replace")
        # print(sys.stdin.encoding)
        # os.system("chcp 65001")
        # print(html.content.decode('utf-8').replace(u'\xa0',' '))
        print(html.text)

spi=PHONE_Spider()
spi.get_html()