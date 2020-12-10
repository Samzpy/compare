from django.shortcuts import render
from django.http import JsonResponse
from tools.login_check import login_check
from user.models import UserProfile
from commodity.models import Commodity
import json
# Create your views here.

@login_check('GET',"DELETE")
def mylist(request):
    if request.method=="GET":          
        user=request.user

        commodity=user.commodity_set.all()
        com_list=[]
        for com in commodity:
            if int(com.com_exist) == 1:
                price=com.com_price
                picture=com.com_picture
                name=com.com_name
                com_id=com.id
                com_list.append({'com_name':name,'com_price':price,'com_picture':picture,'com_id':com_id})
        result={'code':200,'mylist':com_list}
        return JsonResponse(result)

    elif request.method=="DELETE":
        json_str=request.body.decode()
        if not json_str:
            result={'code':301,'error':'Please give me json'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        com_id=json_obj.get('com_id')
        user=request.user
        try:
            com=Commodity.objects.get(id=com_id)
            user.commodity_set.remove(com)
        except:
            result={'code':302,'error':'系統忙碌中'}
            return JsonResponse(result)

        result={'code':200}
        return JsonResponse(result)
