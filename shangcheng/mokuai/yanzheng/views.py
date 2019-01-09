from random import randint

from django.http import HttpResponse
from django.shortcuts import render
from django_redis import get_redis_connection
# Create your views here.
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from disanfang.captcha.captcha import captcha
from disanfang.yuntongxun.sms import CCP
from yanzheng.xuliehua import SjYzmXlh


class Yzm(APIView):
    def get(self,requ,image_code_id):

        text,content=captcha.generate_captcha()
        r_cli=get_redis_connection('code')
        r_cli.setex('yzm_%s'%image_code_id,600,text)

        return HttpResponse(content,content_type='image/jpeg')
class SjYzm(APIView):
    def get(self,requ,mobile):
        dat=requ.query_params
        s=SjYzmXlh(data=dat)
        s.is_valid(raise_exception=True)
        dxyzm='%06d'%randint(0,999999)
        # from celery_tasks.duanxin.tasks import fsdxyzm
        # delay 的参数和 任务的参数对应
        # 必须调用 delay 方法
        # fsdxyzm.dalay(mobile,dxyzm)
        # from clery_tasks.sms.tasks import send_sms_code
        # send_sms_code.delay(mobile, dxyzm)
        r_c=get_redis_connection('code')
        try:
            r_c.setex('sjyzm_%s'%mobile,300,dxyzm)
        except:
            return Response(status=400)
        from celery_tasks.duanxin.tasks import fsdxyzm
        fsdxyzm.delay(mobile,dxyzm)

        print(dxyzm)
        return Response({'message':'ok'})


