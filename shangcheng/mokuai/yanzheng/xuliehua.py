from redis import RedisError
from rest_framework import serializers
from django_redis import get_redis_connection

from gonggong.yichangchuli import logger


class SjYzmXlh(serializers.Serializer):
    text=serializers.CharField(max_length=4,min_length=4,required=True)
    # uuid=serializers.UUIDField(label='id```')
    # text = serializers.CharField(label='用户输入的验证码', max_length=4, min_length=4, required=True)
    image_code_id = serializers.UUIDField(label='验证码唯一性id')

    def validate(self, attrs):
        uuid=attrs['image_code_id']
        text=attrs['text']
        r_c=get_redis_connection('code')
        textt=r_c.get('yzm_%s'%str(uuid))
        if textt is None:
            raise serializers.ValidationError('验证嗯国企')
        try:
            r_c.delete('yzm_%s'%str(uuid))
        except Exception as e:
            logger.error(e)
        if textt.decode().lower() != text.lower():
            raise serializers.ValidationError('输入验证嗯码错误')
        return attrs
#
#
# from rest_framework import serializers
# from django_redis import get_redis_connection
# from redis.exceptions import RedisError
# import logging
#
# logger = logging.getLogger('meiduo')
#
#
# class RegisterSMSCodeSerializer(serializers.Serializer):
#     """
#     校验 验证码和image_code_id
#     """
#

#
#     #我们需要用到这两个字段,所以在validate中进行判断
#     def validate(self, attrs):
#
#         #获取用户提交的验证码
#         text = attrs['text']
#         image_code_id = attrs['image_code_id']
#         #链接redis,获取redis中的验证码
#         redis_conn = get_redis_connection('code')
#         redis_text = redis_conn.get('img_%s'%image_code_id)
#         # 判断从redis中获取的验证码是否存在
#         if redis_text is None:
#             raise serializers.ValidationError('验证码已过期')
#         #将redis中的验证码删除
#         try:
#             redis_conn.delete('img_%s'%image_code_id)
#         except RedisError as e:
#             logger.error(e)
#         #对redis的验证码编码之后进行比对,要注意大小写问题
#         if redis_text.decode().lower() != text.lower():
#             raise serializers.ValidationError('验证码错误')
#
#         return attrs