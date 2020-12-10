from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username=models.CharField('用戶姓名',max_length=11)
    password = models.CharField(max_length=32, verbose_name='用戶密碼')
    email = models.EmailField(max_length=32, verbose_name='email')
    

    class Meta:
        db_table = 'user_profile'
