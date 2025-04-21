from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class User(models.Model):
    id = models.AutoField('id',primary_key=True)
    username = models.CharField('username',max_length=50,default='')
    password = models.CharField('password',max_length=50,default='')
    createTime = models.DateTimeField('create time',auto_now_add=True)

    class Meta:
        db_table = 'user'

class History(models.Model):
    id = models.AutoField('id',primary_key=True)
    movie_id = models.CharField('movie_id',max_length=50,default='')
    count = models.IntegerField('收藏cishu',default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='history')

    class Meta:
        db_table = 'history'



