from django.db import models
from user.models import UserProfile

# Create your models here.
class Message(models.Model):
    content = models.CharField(max_length=500, verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(UserProfile)

    class Meta:
        db_table = 'message'