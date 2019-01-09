from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
# def cs(requ):
#     from django.db import DatabaseError
#     raise DatabaseError('error')
#     return HttpResponse('ok')
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from disanfang.captcha.captcha import captcha
from yonghu.models import Yhb
from yonghu.xuliehua import YhbXlh


class YhmYz(APIView):
    # 用户名验证
    def get(self,requ,username):
        count=Yhb.objects.filter(username=username).count()
        return Response({'count':count})
class YhmMobile(APIView):
    # 手机号验证
    def get(self,requ,mobile):
        count=Yhb.objects.filter(mobile=mobile).count()
        return Response({'count':count})
class YhZc(APIView):
    def post(self,requ):
        dat=requ.data
        s=YhbXlh(data=dat)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)





