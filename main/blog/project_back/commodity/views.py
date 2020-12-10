from django.shortcuts import render
from django.http import JsonResponse
from .models import Commodity,Mall
import random

# Create your views here.
def commodity(request):
    if request.method == "GET":
        mall_list=[]
        exam_choice_list = random.sample([i for i in range(1,896)], 15)

        for i in exam_choice_list:
            mall_detail=[]
            try:
                #新增一個判定com_exist 指定 為1
                commodity=Commodity.objects.get(id=i,com_exist=1)
            except:
                continue
            if commodity:
                com_name=commodity.com_name
                com_img=commodity.com_picture.replace(" ","%20")
                malls=commodity.mall_set.order_by("com_price")[:3]  
                for mall in malls:
                    mall_detail.append({'mall_price':mall.com_price,'mall_name':mall.mall_name,'mall_url':mall.com_web_url})
            if not mall_detail:
                continue
            mall_list.append({'picture':com_img,'com_name':com_name,'com_id':i,'mall_list':mall_detail})
    

    return JsonResponse({"code":200,'commodity':mall_list})

def commodity_sort(request,com_sort=None):
    if request.method == "GET":
        if com_sort:
            com_brand=request.GET.get('brand','')
            com_pg=request.GET.get('pg','')
            com_pg=(int(com_pg)-1)*20
            if com_brand =='all':
                commodity_all=Commodity.objects.filter(com_sort=com_sort,com_exist=1)
                lenght=commodity_all.count()
                total_pg=(lenght//20) 
                commodity_all=commodity_all[com_pg:lenght][:20]      
                commodity_all=random.sample(list(commodity_all),len(list(commodity_all)))
            else:
                commodity_all=Commodity.objects.filter(com_sort=com_sort,com_exist=1,com_brand=com_brand)
                lenght=commodity_all.count()
                total_pg=(lenght//20) 
                commodity_all=commodity_all[com_pg:lenght][:20]     
            mall_list=[]
            if commodity_all:
                for commodity in commodity_all:
                    mall_detail=[]
                    com_name=commodity.com_name
                    com_img=commodity.com_picture.replace(" ","%20")
                    malls=commodity.mall_set.order_by("com_price")[:3]
                    for mall in malls:
                        mall_detail.append({'mall_price':mall.com_price,'mall_name':mall.mall_name,'mall_url':mall.com_web_url})
                    if not mall_detail:
                        continue
                    mall_list.append({'picture':com_img,'com_name':com_name,'com_id':commodity.id,'mall_list':mall_detail})
                    
            else:
                print(commodity_all)
                result={'code':404,'error':'oops'}
                return JsonResponse(result)
        
        return JsonResponse({"code":200,'commodity':mall_list,"total_pg":total_pg})


def commodity_search(request):
    if request.method == "GET":
        com_keyword=request.GET.get('keyword','')
        if com_keyword:
            commodity_all=Commodity.objects.filter(com_name__icontains=com_keyword)
            print(commodity_all)
        mall_list=[]
        if commodity_all:
            for commodity in commodity_all:
                mall_detail=[]
                com_name=commodity.com_name
                com_img=commodity.com_picture.replace(" ","%20")
                malls=commodity.mall_set.order_by("com_price")[:3]
                for mall in malls:
                    mall_detail.append({'mall_price':mall.com_price,'mall_name':mall.mall_name,'mall_url':mall.com_web_url})
                if not mall_detail:
                    continue
                mall_list.append({'picture':com_img,'com_name':com_name,'com_id':commodity.id,'mall_list':mall_detail})
                    
        else:
            print(commodity_all)
            result={'code':404,'error':'oops'}
            return JsonResponse(result)
        
        return JsonResponse({"code":200,'commodity':mall_list})

            

