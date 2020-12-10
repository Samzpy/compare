from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import jwt,time
import json
import hashlib
from .models import UserProfile
from tools.login_check import *
# Create your views here.

#用戶註冊
# @login_check('PUT')
def user_register(request,username=None):
    if request.method == "GET":
        pass
    elif request.method=='POST':
        #創建用戶
        #前端註冊頁面地址 http://127.0.0.1:5000/register
        # {'username':username, 'email':email, 'password_1':password_1, 'password_2':password_2}
        json_str=request.body.decode()
        json_obj=json.loads(json_str)
        username=json_obj.get('username','')
        email=json_obj.get('email','')
        password1=json_obj.get('password_1','')
        password2=json_obj.get('password_2','')
        if not json_str:
            return JsonResponse({'code':205,'error':'no data'})
        if username =="" and len(username) <6:
            return JsonResponse({'code':201,'error':'用戶名長度須大於6'})
        if email =="" and '@'not in email:
            return JsonResponse({'code':202,'error':'尚未填寫信箱 或 格式錯誤'})
        if password1 =="" and len(password1)<6:
            return JsonResponse({'code':203,'error':'尚未填寫密碼一或長度小於6'})
        if password2 =="" and len(password2)<6:
            return JsonResponse({'code':204,'error':'尚未填寫密碼二或長度小於6'})
        if password1 != password2:
            return JsonResponse({'code':204,'error':'重複密碼須相同'})
        #優先查詢當前用戶名是否存在
        old_user=UserProfile.objects.filter(username=username)
        #filter 返回集合 找不到空   get找不到則報做 返回單元訴
        if old_user:
            result ={'code':206,'error':'Your username is already exist'}
            return JsonResponse(result)
        #密碼處理 md5哈西/散列
        m=hashlib.md5()
        m.update(password1.encode())
        #==========charfield 盡量避免使用 null=True
        try:
            UserProfile.objects.create(username=username,password=m.hexdigest(),email=email)
        #用戶名重複 或 數據庫down
        except Exception as e:
            result={'code':207,'error':'Sever is busy'}
            return JsonResponse(result)

        #make token
        token=make_token(username)
        #正常返回前端
        result={'code':200,'username':username,'data':{'token':token.decode()}}
        return JsonResponse(result)


#用戶登入

def user_login(request):
    if not request.method =='POST':
        result={'code':101,'error':'Please use POST'}
        return JsonResponse(result)
    #前端地址 https://127.0.0.1:5000/login
    #獲取前端傳來的數據/生成token
    #獲取-效驗密碼-生成token

    json_str=request.body.decode()
    if not json_str:
        result={'code':102,'error':'Please give me json'}
        return JsonResponse(result)
    json_obj=json.loads(json_str)
    username=json_obj.get('username',"")
    if not username:
        result={'code':103,'error':'請輸入使用者名稱'}
        return JsonResponse(result)
    password=json_obj.get('password',"")
    if not password:
        result={'code':104,'error':'請輸入密碼'}
        return JsonResponse(result)

    #效驗數據====
    user=UserProfile.objects.filter(username=username)
    if not user:
        #故意說用戶或密碼錯 防止有心人士
        result = {'code':105,'error':'用戶或密碼錯誤!!'}
        return JsonResponse(result)

    user=user[0]
    m=hashlib.md5()
    m.update(password.encode())
    if m.hexdigest()!=user.password:
        result = {'code':106,'error':'用戶或密碼錯誤!!'}
        return JsonResponse(result)
    #make token
    token=make_token(username)
    result={'code':200,'username':username,'data':{'token':token.decode()}}
    return JsonResponse(result)


@login_check("GET")
def check_token(request):
    if request.method =="GET":
        return JsonResponse({'code':200})








#將token方法(user) 移出 怕重複代碼)
def make_token(username,expire=60*60*24*7):
    key='1234567'
    now=time.time()
    payload={'username':username,'exp':int(now+expire)}

    return jwt.encode(payload,key,algorithm='HS256')

 # @login_check('POST')
# def users_avatar(request,username):
#     if request.method !='POST':
#         result={'code':212,'error':'I need post'}
#         return JsonResponse(result)
#     avatar=request.FILES.get('avatar','')
#     if not avatar:
#         result={'code':213,'error':'I need avatar'}

#     #TODO 判定url中的username 是否跟 token 中的username是否一直 若否則返回error
#     request.user.avator=avatar
#     request.user.save()
#     result = {'code':200,'username':request.user.username}
#     return JsonResponse(result)