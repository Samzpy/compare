#login_check('PUT',"GET",'POST')
from django.http import JsonResponse
import jwt
from user.models import UserProfile
#_login_check('PUT','GET','POST')
KEY='1234567'
def login_check(*methods):
    def _login_check(func):
        def wrapper(request,*args,**kwargs):
            #通過requesrt 檢查token
            #檢查不通過,return JsonResponse()
            #user查詢出來
            token=request.META.get('HTTP_AUTHORIZATION')
            if request.method not in methods:
                return func(request,*args,**kwargs)
            if not token:
                result={'code':107,'error':'please give me token'}
                return JsonResponse(result)
            try:
                res=jwt.decode(token,KEY,algorithms=['HS256'])
            except jwt.ExpiredSignature:
                #token過期了
                result={'code':108,'error':'Please login'}
                return JsonResponse(result)
            except Exception as e:
                result={'code':109,'error':'Please login'}
                return JsonResponse(result)
            username=res['username']
            try:
                user=UserProfile.objects.get(username=username)
            except:
                user=None
            if not user:
                result={"code":110,"error":"username is not exist"}
                return JsonResponse(result)
            #將request的屬性新增request.user 返回給request
            request.user=user
            return func(request,*args,**kwargs)
        return wrapper
    return _login_check


def get_user_by_request(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res = jwt.decode(token, KEY)
    except:
        return None
    username = res['username']
    try:
        user = UserProfile.objects.get(username=username)
    except:
        return None

    return user