import base64
import json
import pickle
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from cart.xuliehua import GwcXlh, GwclbXlh
from goods.models import SKU
from goods.xuliehua import HotSKUListSerializer


class carts(APIView):
    """
    1.加入购物车
    2.是否登录
    2.0 登录用户---1获取用户id 2商品id 3商品数量 4选中状态

    """
    def perform_authentication(self, request):

        pass
    def post(self,requ):
        data = requ.data  # {'sku_id': 16, 'count': 1}
        s = GwcXlh(data=data)
        s.is_valid(raise_exception=True)
        sku_id = s.validated_data.get('sku_id')
        count = s.validated_data.get('count')
        selected = s.validated_data.get('selected')

        try:
            yh=requ.user
        except:
            yh=None
        if (yh is not None) and (yh.is_authenticated):
            #用户登录
            s.validated_data['yh'] =yh.id
            s.save()
            return Response(s.data)
        else:
            #无效用户或未登录

            cart_str=requ.COOKIES.get('cart')
            if cart_str is not None:
                cart_dict=pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict={}
            if sku_id in cart_dict:
                cart_dict[sku_id]['count']+=count
            else:
                cart_dict[sku_id]={'count':count,'selected':selected}
            resp=Response(s.data)
            cookie_cart = base64.b64encode(pickle.dumps(cart_dict)).decode()
            resp.set_cookie('cart',cookie_cart)
            return resp


    def get(self,requ):

        try:
            yh = requ.user
        except:
            yh = None
        if (yh is not None) and (yh.is_authenticated):
            r_c=get_redis_connection('gwc')
            cart_str=r_c.get(yh.id)
            globals = {
                'true': True
            }
            if cart_str is None:
                return Response(status=203)
            cart_dict=eval(cart_str,globals)

            skus = cart_dict.keys()
            skus = SKU.objects.filter(id__in=skus)
            for i in skus:
                i.count = cart_dict[str(i.id)]['count']
                i.selected = cart_dict[str(i.id)]['selected']


            # #s 用户登录
            # s.validated_data['yh'] = yh.id
            # s.save()
            # return Response(s.data)
        else:
            # 无效用户或未登录

            cart_str = requ.COOKIES.get('cart')
            if cart_str is not None:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}
            skus=cart_dict.keys()
            skus=SKU.objects.filter(id__in=skus)
            for i in skus:
                i.count=cart_dict[i.id]['count']
                i.selected=cart_dict[i.id]['selected']
        s=GwclbXlh(instance=skus,many=True)
        return Response(s.data)

    def put(self, requ):
        # try:
        #     yh = requ.user
        # except:
        #     yh = None
        # if (yh is not None) and (yh.is_authenticated):
        #     #登录
        #     pass
        # else:
        #     #未登录
        #     pass

        data = requ.data
        s=GwcXlh(data=data)
        s.is_valid(raise_exception=True)

        try:
            yh = requ.user
        except:
            yh = None
        if (yh is not None) and (yh.is_authenticated):
            #登录
            r_c = get_redis_connection('gwc')
            cart_str = r_c.get(yh.id)
            globals = {
                'true': 0
            }
            cart_dict = eval(cart_str,globals)
            if str(data['sku_id']) in cart_dict.keys():
                pass
                cart_dict[str(data['sku_id'])]['count']=data['count']
                cart_dict[str(data['sku_id'])]['selected'] = data['selected']
                r_c.set(yh.id,cart_dict)
                return Response(s.data)
            else:
                return Response(status=400)
        else:
            #未登录
            cart_str = requ.COOKIES.get('cart')
            if cart_str is not None:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}
            skus = cart_dict.keys()
            if data['sku_id'] in cart_dict:
                cart_dict[data['sku_id']]['count']=data['count']
                cart_dict[data['sku_id']]['selected'] = data['selected']
                resp=Response(s.data)
                # cart_dict=pickle.dumps(base64.b64encode(cart_dict))
                cookie_cart = base64.b64encode(pickle.dumps(cart_dict)).decode()
                resp.set_cookie('cart',cookie_cart)
                return resp

        #     skus = SKU.objects.filter(id__in=skus)
        #     for i in skus:
        #         i.count = cart_dict[i.id]['count']
        #         i.selected = cart_dict[i.id]['selected']
        # s = GwclbXlh(instance=skus, many=True)
        # return Response(s.data)


    def delete(self,requ):
        data=requ.data
        try:
            yh = requ.user
        except:
            yh = None
        if (yh is not None) and (yh.is_authenticated):
            #登录
            r_c = get_redis_connection('gwc')
            cart_str = r_c.get(yh.id)
            globals = {
                'true': 0
            }
            cart_dict = eval(cart_str, globals)
            sku_id=data.get('sku_id')
            sku_id=18
            if not str(sku_id) in cart_dict.keys():
                return Response(status=204)
            del  cart_dict['%s'%sku_id]
            r_c.set(yh.id,cart_dict)
            return Response(status=203)

        else:
            #未登录
            cart_str = requ.COOKIES.get('cart')
            if cart_str is not None:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
                if data['sku_id'] in cart_dict:
                    del cart_dict[data['sku_id']]
                    resp=Response(status=204)
                    cookie_cart = base64.b64encode(pickle.dumps(cart_dict)).decode()
                    resp.set_cookie('cart',cookie_cart)
                    return resp

