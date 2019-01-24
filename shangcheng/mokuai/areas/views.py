from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import   ReadOnlyModelViewSet
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas.models import Area
from areas.xuliehua import ShangXlh, XiaXlh


class ShengFen(APIView):
    @cache_response(timeout=60 * 60, cache='default')
    def get(self,requ):
        shengfen=Area.objects.filter(parent__isnull=True)
        s=ShangXlh(shengfen,many=True)
        return Response(s.data)
class ShiXian(APIView):
    def get(self,requ,shang):
        shengfen = Area.objects.filter(parent=shang)
        s = ShangXlh(shengfen,many=True)
        return Response(s.data)
class ChengShi(ReadOnlyModelViewSet):
    def get_queryset(self):
        method=self.action
        if method=='list':
            queryset=Area.objects.filter(parent__isnull=True)
        else:
            queryset=Area.objects.all()
        return queryset

    # serializer_class = ShangXlh
    def get_serializer_class(self):
        if self.action=='list':
            serializer_class = ShangXlh
        else:
            serializer_class=XiaXlh
        return serializer_class
# class ChengShi(CacheResponseMixin,ReadOnlyModelViewSet):
#
#     # queryset = Area.objects.all()   #所有信息
#     # queryset = Area.objects.filter(parent=None)   #省的信息
#
#     def get_queryset(self):
#
#         # 我们可以根据 不同的业务逻辑返回不同的数据源
#         if self.action == 'list':
#             # Area.objects.filter(parent__isnull=True)
#             return Area.objects.filter(parent=None)
#         else:
#             return Area.objects.all()
#
#     # serializer_class = AreaSerializer
#
#     def get_serializer_class(self):
#
#         # 我们可以根据 不同的业务逻辑返回不同的 序列化器
#         if self.action == 'list':
#             return ShangXlh
#         else:
#             return XiaXlh
