from django.http import HttpResponse
from django.shortcuts import render
from django_redis import get_redis_connection
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

from cart.cart_gg import hebing
from disanfang.captcha.captcha import captcha
from goods.models import SKU
from goods.xuliehua import HotSKUListSerializer
from yonghu.models import Yhb, Address
from yonghu.xuliehua import YhbXlh, EmailsXlh, YhLlXlh, addressxlh
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

"""浏览历史
记录用户浏览的商品

"""
class YhLl(CreateAPIView):
    serializer_class = YhLlXlh
    permission_classes = [IsAuthenticated]
    def get(self,request):
        yhid=request.user
        r_c=get_redis_connection('yhlljl')
        skus=r_c.lrange('history_%s'%yhid,0,-1)
        sku=[]
        for f in skus:
            a=SKU.objects.get(id=f)
            sku.append(a)
        s=HotSKUListSerializer(sku,many=True)
        return Response(s.data)

from rest_framework_jwt.views import ObtainJSONWebToken

class MergeLoginAPIView(ObtainJSONWebToken):


    def post(self, request, *args, **kwargs):
        # 调用jwt扩展的方法，对用户登录的数据进行验证
        response = super().post(request)

        # 如果用户登录成功，进行购物车数据合并
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 表示用户登录成功
            user = serializer.validated_data.get("user")
            # 合并购物车
            # merge_cart_cookie_to_redis(request, user, response)
            response = hebing(request, user, response)

        return response
class address(APIView):
    def get(self,requ):
        ads=Address.objects.all()
        s=addressxlh(ads,many=True)
        return Response({'addresses':s.data,'default_address_id':1})
