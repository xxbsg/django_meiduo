from django.utils import timezone

from decimal import Decimal

from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import serializers

from goods.models import SKU
from goods.xuliehua import HotSKUListSerializer


# class select_goodsxlh(serializers.Serializer):
#     skus=HotSKUListSerializer()
#     freight=serializers.IntegerField(d)
#     total_count=1
#     total_amount=1
from orders.models import OrderInfo, OrderGoods


class OrderCommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'address', 'pay_method')
        read_only_fields = ('order_id',)
        extra_kwargs = {
            'address': {
                'write_only': True,
                'required': True,
            },
            'pay_method': {
                'write_only': True,
                'required': True
            }
        }

    def create(self, validated_data):
        """保存订单"""

        # 获取当前下单用户
        user = self.context['request'].user
        # 生成订单编号
        # 保存订单的基本信息数据 OrderInfo
        # 创建订单编号
        # 20180523160505+ user_id  100
        # timezone.now() -> datetime

        order_id = timezone.now().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)

        # 保存订单基本信息数据 OrderInfo
        address = validated_data['address']
        pay_method = validated_data['pay_method']
        with transaction.atomic():
            '开启事物点'
            save_id = transaction.savepoint()
            try:
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal('0'),
                    freight=Decimal('10.0'),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNSEND'] if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH'] else
                    OrderInfo.ORDER_STATUS_ENUM['UNPAID']
                )

                # 从redis中获取购物车结算商品数据
                redis_conn = get_redis_connection('gwc')

                cart_str=redis_conn.get(user.id)
                cart_dict=eval(cart_str,{'true':True})
                #{商品id:{'count':3,'selected':True},商品id:{'count':3,'selected':True}}
                # 遍历结算商品：
                cart = {}

                for sku_id,s_c in cart_dict.items():
                    if s_c['selected']:
                        cart[int(sku_id)] = int(s_c['count'])

                sku_id_list = cart.keys()

                for sku_id in sku_id_list:
                    while True:
                        sku = SKU.objects.get(pk=sku_id)
                        # 判断商品库存是否充足
                        count = cart[sku.id]
                        if sku.stock < count:
                            raise serializers.ValidationError('库存不足')
                        # 减少商品库存，增加商品销量
                        sku.stock -= count
                        sku.sales += count
                        sku.save()
                        # 保存订单商品数据
                        order.total_count += count
                        order.total_amount += (sku.price * count)

                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            count=count,
                            price=sku.price
                        )
                        break
                order.save()
            except ValueError:
                raise
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                raise serializers.ValidationError('下单失败')

            # 清除购物车中已经结算的商品
            pl = redis_conn.pipeline()
            # pl.hdel('cart_%s' % user.id, *cart_selected)
            # pl.srem('cart_selected_%s' % user.id, *cart_selected)
            pl.delete(user.id)
            pl.execute()

            return order