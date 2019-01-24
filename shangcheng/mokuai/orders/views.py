from django.shortcuts import render
from django_redis import get_redis_connection
# Create your views here.
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.xuliehua import GwclbXlh
from goods.models import SKU
# from orders.xueliehua import select_goodsxlh
from orders.xueliehua import OrderCommitSerializer


class select_goods(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,requ):
        yh=requ.user
        r_c=get_redis_connection('gwc')
        r_str=r_c.get(yh.id)
        if r_str is None:
            return Response(status=204)

        r_dict=eval(r_str,{'true':True})
        skus = r_dict.keys()
        skus = SKU.objects.filter(id__in=skus)

        for i in skus:
            i.count = r_dict[str(i.id)]['count']
            i.selected = r_dict[str(i.id)]['selected']
        s = GwclbXlh(instance=skus, many=True)
        return Response({'skus':s.data,'freight':10,})
class OrderView(CreateAPIView):
    """
    保存订单
    POST /orders/

    登录用户
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCommitSerializer