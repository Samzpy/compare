from django.shortcuts import render
from django.http import JsonResponse
# from .models import Commodity,Mall
from commodity.models import Commodity,Mall
from tools.login_check import *
import json
# Create your views here.
@login_check("PUT")
def com_detail(request):
    if request.method == "GET":
        #獲取商品id
        com_id=request.GET.get('com_id','')
        #檢驗商品是否為追蹤狀態
        user=get_user_by_request(request)
        if user:
            user_track=user.commodity_set.filter(id=com_id)
            if user_track:
                com_track=1
            else:
                com_track=0
        else:
            com_track=0
        #獲取商品資訊
        try:
            commodity=Commodity.objects.get(id=com_id,com_exist=1)
        except Exception as e:
            print(e)
            return JsonResponse({'code':404})
        com_name=commodity.com_name
        com_price=commodity.com_price
        com_img=commodity.com_picture.replace(" ","%20")
        malls=commodity.mall_set.order_by('com_price')
        mall_detail=[]
        for mall in malls:
            mall_detail.append({'mall_price':mall.com_price,'mall_name':mall.mall_name,'mall_url':mall.com_web_url,'mall_com_name':mall.com_name})
        return JsonResponse({"code":200,'com_name':com_name,'commodity':mall_detail,'com_track':com_track,'com_price':com_price,'com_img':com_img})
    elif request.method =="PUT":
        json_str=request.body.decode()
        if not json_str:
            result={'code':301,'error':'Please give me json'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        com_id=json_obj.get('com_id')
        com=Commodity.objects.get(id=com_id)
        user=request.user
        if user:
            user_track=user.commodity_set.filter(id=com_id)
            if user_track:
                user.commodity_set.remove(com)
                com_track=0
            else:
                user.commodity_set.add(com)
                com_track=1           
        else:
            result={'code':301,'error':'Please give me json'}
            return JsonResponse(result)
        
        return JsonResponse({'code':200,'com_track':com_track})




