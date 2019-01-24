from django.db import models

# Create your models here.
from gonggong.models import BaseModel


class QqYhb(BaseModel):
    openid=models.CharField(max_length=64,verbose_name='openid',db_index=True,unique=True)
    user=models.ForeignKey('yonghu.Yhb',on_delete=models.CASCADE,verbose_name='用户')
    class Meta:
        db_table='t_qqyhb'
        verbose_name='qq登录数据'
        verbose_name_plural=verbose_name