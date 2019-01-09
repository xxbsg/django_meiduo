from rest_framework import serializers
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings

from yonghu.models import Yhb


class YhbXlh(serializers.ModelSerializer):
    '''
                        # username: this.username,
                        # password: this.password,
                        password2: this.password2,
                        # mobile: this.mobile,
                        sms_code: this.sms_code,
                        allow: this.allow.toString()

    '''
    password2=serializers.CharField(max_length=20,min_length=3,required=True,write_only=True)
    sms_code=serializers.CharField(max_length=6,min_length=6,required=True,write_only=True)
    allow=serializers.CharField(required=True,write_only=True)
    token=serializers.CharField(read_only=True)
    class Meta:
        model=Yhb
        fields =['username','password','mobile','password2','sms_code','allow','id','token']
        # 返回数据时不能返回密码,但需要返回id 所以重写id password字段
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }
    def validate(self, attrs):
        username=attrs.get('username')
        password=attrs.get('password')
        mobile=attrs.get('mobile')
        password2=attrs.get('password2')
        sms_code=attrs.get('sms_code')
        allow=attrs.get('allow')
        if not all([username,password,mobile,password2,sms_code,allow]):
            raise serializers.ValidationError('数据不能为空')
        if password2!=password:
            raise serializers.ValidationError('两次输入不一致')
        if allow !='true':
            raise  serializers.ValidationError('请先统一')
        r_c=get_redis_connection('code')
        sjyzm=r_c.get('sjyzm_%s'%mobile)
        r_c.delete('sjyzm_%s'%mobile)
        if sjyzm.decode()!=sms_code:
            raise serializers.ValidationError('短信验证嗯错误,请重新发送')

        return attrs
    def create(self, validated_data):

        validated_data.pop('password2')
        validated_data.pop('sms_code')
        validated_data.pop('allow')
        # instance = self.super().create(validated_data)
        instance=super().create(validated_data)
        instance.set_password(validated_data.get('password'))
        instance.save()
        # 生成token字段返回
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(instance)
        token = jwt_encode_handler(payload)
        instance.token = token
        return instance



