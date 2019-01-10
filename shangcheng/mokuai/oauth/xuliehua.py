import re

from django_redis import get_redis_connection
from rest_framework import serializers

from oauth.models import QqYhb
from oauth.oa_gg import jopenid
from yonghu.models import Yhb


class qqyhxlh(serializers.Serializer):
    sms_code = serializers.CharField(max_length=6, min_length=6, required=True, write_only=True)
    mobile=serializers.CharField(max_length=11, min_length=11, required=True,)
    password=serializers.CharField(max_length=20, min_length=3, required=True,write_only=True)
    access_token=serializers.CharField(required=True)
    def validate(self, attrs):
        token=attrs.get('access_token')
        sms_code=attrs.get('sms_code')
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        token=jopenid(token)
        attrs['token']=token
        if token is None:
            return serializers.ValidationError('openid错误')

        # 判断验证嗯码
        r_c = get_redis_connection('code')
        sjyzm = r_c.get('sjyzm_%s' % mobile)
        r_c.delete('sjyzm_%s' % mobile)
        if sjyzm.decode() != sms_code:
            raise serializers.ValidationError('短信验证嗯错误,请重新发送')

        if not re.match(r'1[3-9]\d{9}',mobile) :
            return serializers.ValidationError('手机号错误')
        try:
            yh=Yhb.objects.get(mobile=mobile)
        except:
            return attrs
    #       创建用户

        else:
            if not yh.check_password(password):
                return serializers.ValidationError('密码错误')
            else:
                attrs['user']=yh
    #         关联用户
            return attrs
    def create(self, validated_data):
        if validated_data.get('user'):
            qyh=QqYhb.objects.create(openid=validated_data.get('token'),user_id=validated_data.get('user').id)
            qyh.save()
            return qyh
        else:
            mobile = validated_data.get('mobile')
            password = validated_data.get('password')
            yh=Yhb.objects.create(mobile=mobile,password=password,username=mobile)
            yh.save()
            qyh=QqYhb.objects.create(user_id=yh.id,openid=validated_data.get('token'))
            qyh.save()
            return qyh

