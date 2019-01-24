from django.contrib import admin

# Register your models here.
from yonghu.models import Yhb, Address

admin.site.register(Yhb)#注册显示用户表
admin.site.register(Address)
