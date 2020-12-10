import pymysql

class Info_Mysql:
    def __init__(self,commodify_info):
        self.commodify_info=commodify_info
        config={
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'a123456',
            'db':'final_project',
        }
        self.connection=pymysql.connect(**config)


    def commodify_get_info(self):
        with self.connection.cursor() as cursor:
            sql="select com_number from commodity"
            cursor.execute(sql)
            result =cursor.fetchall()
            self.commodify_parse_info(result)
            sql="select com_number from commodity where com_brand = '%s' and com_sort='%s'"%(self.commodify_info[0][0],self.commodify_info[0][1])
            cursor.execute(sql)
            result =cursor.fetchall()
            self.commodify_modify_info(result)

    
    def commodify_parse_info(self,result):
        with self.connection.cursor() as cursor:

        # apple,手機,iPhone SE（第 2 代）64GB;iPhone SE（第 2 代）64GB,https://support.apple.com//library/content/dam/edam/applecare/images/en_US/iphone/iphone_se/iphone-se-2nd-gen-colors.jpg
          #品牌,分類,商品名稱;商品編號,圖片
        # a= [i for i in A if i in [j for j in B]]       #爬蟲有 數據庫有
        # b= [i for i in A if i  not in [j for j in B]]  #爬   蟲有 數據庫沒有
        # c= [i for i in B if i  not in [j for j in A]]  #爬蟲沒有 數據庫 有    
        #   
        #爬   蟲有 數據庫沒有
            insert_=[i for i in self.commodify_info if i[3]  not in [j[0] for j in result] ]   
            for i in insert_:
                #品牌,分類,商品名稱,編碼,關鍵字索引,圖片
                com_brand=i[0]
                com_sort=i[1]
                com_name=i[2]
                com_number=i[3]
                com_keyword=i[4]
                com_price='0~0'
                com_exist='1'
                com_picture=i[5]

                sql='insert into commodity(com_brand,com_sort,com_name,com_number,com_keyword,com_price,com_exist,com_picture) values ("%s","%s","%s","%s","%s","%s","%s","%s")' %(com_brand,com_sort,com_name,com_number,com_keyword,com_price,com_exist,com_picture)
                try:
                    cursor.execute(sql)
                    self.connection.commit()
                    # sql='select id from commodity where com_number= "%s"'%com_number
                    # cursor.execute(sql)
                    # mtm =cursor.fetchall()
                    # if mtm:
                    #     mtm=mtm[0][0]
                    #     sql='insert into commodity_com_follower(commodity_id,userprofile_id) values (%s,1)' %int(mtm)
                    #     cursor.execute(sql)
                    #     self.connection.commit()
                except Exception as e:
                    self.connection.rollback()
                    print(sql)
                    print(e)
    
    #爬蟲沒有 數據庫 有
    def commodify_modify_info(self,result):
        with self.connection.cursor() as cursor:
            modify=[j[0] for j in result if j[0] not in [i[3] for i in self.commodify_info]] 
            for i in modify:
                sql = 'update commodity set com_exist="0" where com_number = "%s"'% i
                try:
                    cursor.execute(sql)
                    self.connection.commit()
                except Exception as e:
                    self.connection.rollback()
                    print(e)


# aa=Info_Mysql(0,'tt')
# aa.commodify_get_info()

