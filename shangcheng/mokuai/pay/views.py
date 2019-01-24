from django.shortcuts import render

# Create your views here.
from alipay import AliPay
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import OrderInfo
from shangcheng.settings import ALI, APPA


class pay(APIView):
    def get(self,request,orders_id):
        user = request.user
        # 判断订单是否正确
        try:
            order = OrderInfo.objects.get(order_id=orders_id,
                                          user=user,
                                          status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return Response({'message': '订单信息有误'}, status=status.HTTP_400_BAD_REQUEST)

        app_private_key_string = open('/home/python/Desktop/django/django_meiduo/shangcheng/gonggong/key/app_private_key.pem').read()
        alipay_public_key_string = open('/home/python/Desktop/django/django_meiduo/shangcheng/gonggong/key/alipay_public_key.pem').read()

        # app_private_key_string == """
        #     -----BEGIN RSA PRIVATE KEY-----
        #     base64 encoded content
        #     -----END RSA PRIVATE KEY-----
        # """
        #
        # alipay_public_key_string == """
        #     -----BEGIN PUBLIC KEY-----
        #     base64 encoded content
        #     -----END PUBLIC KEY-----
        # """
        #
        alipay = AliPay(
            appid="2016092400588286",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2", # RSA 或者 RSA2
            debug=False , # 默认False
        )

        # 如果你是 Python 3的用户，使用默认的字符串即可
        subject = "测试订单"

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=orders_id,
            total_amount=str(order.total_amount),
            subject=subject,
            # return_url="http://www.meiduo.site:8000/pay_success.html",
            return_url="http://www.meiduo.site:8080/pay_success.html"
            # notify_url="https://example.com/notify"  # 可选, 不填则使用默认notify url
        )
        # 构造支付地址
        alipay_url = 'https://openapi.alipaydev.com/gateway.do' + '?' + order_string
        # 返回响应
        return Response({'alipay_url': alipay_url})


