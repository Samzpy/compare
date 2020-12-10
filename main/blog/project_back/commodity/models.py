from django.db import models
from user.models import UserProfile
# Create your models here.
class Commodity(models.Model):
    com_brand=models.CharField('商品品牌',max_length=50)
    com_sort=models.CharField('商品分類',max_length=50)
    com_keyword=models.CharField('商品關鍵字',max_length=50)
    com_name=models.CharField('商品名稱',max_length=300)
    com_price= models.CharField(max_length=32, verbose_name='商品價格範圍',default=0)
    com_number=models.CharField("商品編號",max_length=50)
    com_exist=models.CharField('商品是否存在',max_length=1)
    com_picture=models.CharField('商品圖片',max_length=300)
    com_follower = models.ManyToManyField(UserProfile)

    class Meta:
        db_table = 'commodity'
    

class Mall(models.Model):
    com_name=models.CharField('商品姓名',max_length=100)
    com_price= models.IntegerField(verbose_name="商品價格",)
    mall_name=models.CharField("商城名稱",max_length=100)
    com_web_url=models.CharField("商城網址",max_length=300)
    mall_detail=models.ForeignKey(Commodity)
    class Meta:
        db_table = 'mall'
