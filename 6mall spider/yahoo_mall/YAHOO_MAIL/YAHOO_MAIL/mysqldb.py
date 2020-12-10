import pymysql
import logging
from fake_useragent import UserAgent


def singletonDecorator(cls,*args,**kwargs):
    instance={}
    def wrapperSingleton(*args,**kwargs):
        if cls not in instance:
            instance[cls]=cls(*args,**kwargs)
            logging.info('new instance')
        return instance[cls]
    return wrapperSingleton

@singletonDecorator
class database():
    def __init__(self):
        config={
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'a123456',
            'db':'final_project',
        }
        self.__connection=pymysql.connect(**config)

    def found(self):
        with self.__connection.cursor() as cursor:
            sql='select com_keyword,id from commodity'
            cursor.execute(sql)
            result=cursor.fetchall()
            
        return result
        
    def insert_(self,item):
        result=self.deduplication(item["com_id"])
        #(mall_id, com_name, com_price, mail_name, mall_url, com_id)
        self.__connection.ping()
        with self.__connection.cursor() as cursor:
            #當有重複數據
            if result:
                #數據庫當前價格
                db_price=result[2]
                #新數據價格
                new_price=int(item['price'])
                if new_price<db_price:
                    sql='delete from mall where id="%s"'%result[0]
                    try:
                        cursor.execute(sql)
                        self.__connection.commit()
                    except Exception as e:
                        print(e) 
                        self.__connection.rollback()
                    sql='insert into mall(com_name,com_price,mall_name,com_web_url,mall_detail_id) values ("%s",%s,"%s","%s",%s)' %(item['name'],item['price'],'yahoo超級商城',item['com_url'],item['com_id'])
                    try:
                        cursor.execute(sql)
                        self.__connection.commit()
                    except Exception as e:
                        print(e)
                        self.__connection.rollback()
                
            #當事新數據
            else:
                sql='insert into mall(com_name,com_price,mall_name,com_web_url,mall_detail_id) values ("%s",%s,"%s","%s",%s)' %(item['name'],item['price'],'yahoo超級商城',item['com_url'],item['com_id'])
                try:
                    cursor.execute(sql)
                    self.__connection.commit()
                except Exception as e:
                    print(e)
                    self.__connection.rollback()
    def deduplication(self,com_id):
        self.__connection.ping()
        with self.__connection.cursor() as cursor:
            sql='select * from mall where mall_detail_id= %s and mall_name="yahoo超級商城"' %com_id
            cursor.execute(sql)
            result=cursor.fetchall()
            if result:
                return result[0]



    def close(self):
        self.__connection.close()
