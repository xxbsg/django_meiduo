from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
# def cs(requ):
#     from django.db import DatabaseError
#     raise DatabaseError('error')
#     return HttpResponse('ok')
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from disanfang.captcha.captcha import captcha
from yonghu.models import Yhb
from yonghu.xuliehua import YhbXlh, EmailsXlh
from yonghu.yh_gg import  check_token


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
class YhzxXx(APIView):
    '''
    需要:用户名 手机号 eail (用户登录 id)
    '''
    # Request
    permission_classes = [IsAuthenticated]
    def get(self,requ):
        user=requ.user
        s=YhbXlh(user)
        return Response(s.data)
class Emails(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,requ):
        dat=requ.data
        user=requ.user
        s=EmailsXlh(user,data=dat)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)
class E_active(APIView):
    def get(self,requ):
        token=requ.query_params.get('token')
        if token is None:
            return Response(status=403)
        id=check_token(token)
        try:
            user=Yhb.objects.get(id=id)
        except:
            return Response(status=403)
        user.e_active=True
        user.save()
        return Response({'msg':'ok'})







