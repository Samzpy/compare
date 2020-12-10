from selenium import webdriver
from time import sleep as sl
from selenium.webdriver.chrome.options import Options
import csv
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from parse import Info_Mysql

class crawler:
    def __init__(self):
        chrome_options=Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("window-size=1920,1080")
        self.__drivrer=webdriver.Chrome(chrome_options=chrome_options)
        self.url='https://www.philips.com.tw/c-m-so/tv/latest#layout=96'
    def __close(self):
        sl(0.5)
        self.__drivrer.close()
    def crawl_specific_forum(self):
        name_list=[]
        self.__drivrer.get(self.url)
        sl(1)      
        # js="var q=document.documentElement.scrollTop=100000"
        js = "window.scrollTo(0, document.body.scrollHeight);"  
        self.__drivrer.execute_script(js)  
        sl(1)
        # r_list=self.__drivrer.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div/div[2]/div[3]/div/div/ul/li')
        # for artical in r_list:
        #     try:
        #         name = artical.find_element_by_xpath('.//a/h3').text.replace(' ','')
        #         pn = artical.find_element_by_xpath('.//a/p').text
        #         # .get_attribute('href')
        #         name='Whirlpool惠而浦 '+name+' '+pn
        #         keyword='Whirlpool惠而浦 '+pn
        #         img = artical.find_element_by_xpath('.//div[@class="product-pic"]/a/img').get_attribute('src')
        #         name_list.append(['whirlpool','烤箱',name,pn,keyword,img])
        #     except:
        #         pass
        sl(2)
        li_list=self.__drivrer.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/div/div/div[2]/div[3]/div/div/ul/li')
        for i in li_list:
            try:
                name=i.find_element_by_xpath('.//span[@class="p-heading-light"]').text.strip()
                pn=i.find_element_by_xpath('.//p[@class="p-pc05v2__card-ctn p-body-copy-03 p-heading-light"]').text.strip().replace("/96","")
                name='PHILIPS飛利浦 '+name+' '+pn
                img=i.find_element_by_xpath('.//picture[@class="p-picture p-product-picture"]/img').get_attribute('src')
                keyword='PHILIPS '+pn
                name_list.append(['philips','tv',name,pn,keyword,img])
            except Exception as e:
                print(e)
                pass

        # self.write_csv(name_list)
        self.write_mysql(name_list)
           
           
    def write_csv(self,name_list):
        with open('philps.csv','w',encoding='utf-8',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(name_list)
                
        self.__close()

    def write_mysql(self,name_list):

        mysql=Info_Mysql(name_list)
        mysql.commodify_get_info()
        self.__close()



spi=crawler()
spi.crawl_specific_forum()