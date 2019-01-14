from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Yhb(AbstractUser):
    # 用户表
    mobile=models.CharField(max_length=11,unique=True,verbose_name='手机号')
    e_active=models.BooleanField(default=False,verbose_name='邮件是否激活')
    class Meta:
        db_table='t_yhb'
        verbose_name='用户表'
        verbose_name_plural=verbose_name