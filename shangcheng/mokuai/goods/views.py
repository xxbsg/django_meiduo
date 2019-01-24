from django.shortcuts import render

# Create your views here.
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from goods.models import SKU
from goods.xuliehua import HotSKUListSerializer


class ReXiao(ListAPIView):
    pagination_class = None
    def get_queryset(self):
        queryset = SKU.objects.filter(category_id=self.kwargs.get('leiid')).order_by('-sales')[:3]
        return queryset
    serializer_class = HotSKUListSerializer

class Splb(ListAPIView):
    # pagination_class = None
    filter_backends = [OrderingFilter]
    ordering_fields = ('create_time', 'price', 'sales')
    def get_queryset(self):
        # ordering=self.request.query_params.get('ordering')
        # yeshu=int(self.request.query_params.get('page'))
        # size=int(self.request.query_params.get('page_size'))
        # kaishi=0+(yeshu-1)*size
        # jieshu=kaishi+size
        # queryset=SKU.objects.filter(category_id=self.kwargs.get('leiid')).order_by(ordering)[kaishi:jieshu]
        # return queryset
        return SKU.objects.filter(category_id=self.kwargs.get('leiid'),is_launched=True)
    serializer_class=HotSKUListSerializer


from .xuliehua import SKUIndexSerializer
from drf_haystack.viewsets import HaystackViewSet

class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]

    serializer_class = SKUIndexSerializer