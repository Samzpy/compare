import pymysql

config={
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'a123456',
            'db':'final_project',
        }

#取出com_exist=1 的商品
db=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='a123456',db='final_project')
cursor=db.cursor()
sql='select id from commodity where com_exist=1'
cursor.execute(sql)
result=cursor.fetchall()
# re=[i[0] for i in result]


#查看商品在6mall的價格
for r in result:
    sql='select com_price from mall where mall_detail_id = %s'
    cursor.execute(sql,r)
    re=cursor.fetchall()
    if re:
        price_obj=[i[0] for i in re]
        price_max=str(max(price_obj))
        price_min=str(min(price_obj))
        price='$'+price_min+" ~ "+'$'+price_max
        try:
            sql='update commodity set com_price="{}" where id="{}"'.format(price,r[0])
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()



# print([i[0] for i in result])
# re=list(result)
# for i in re:
#     print(int(i[0]))
# print((max(result))