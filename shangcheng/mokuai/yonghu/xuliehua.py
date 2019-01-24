import re

from django.core.mail import send_mail
from rest_framework import serializers
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings

from celery_tasks.youxiang.tasks import fsyx
from shangcheng import settings
from yonghu.models import Yhb, Address
from yonghu.yh_gg import  generic_verify_url

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
        fields =['username','password','mobile','password2','sms_code','allow','id','token','email','e_active']
        # 返回数据时不能返回密码,但需要返回id 所以重写id password字段
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'required': False,'read_only': True},
            'e_active':{'required': False,'read_only': True},
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

class EmailsXlh(serializers.ModelSerializer):
    class Meta:
        model=Yhb
        fields=['id','email']
        extra_kwargs={'email':{'required':True},}
    def validate(self, attrs):
        if not re.match(r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$',attrs.get('email')):
            return serializers.ValidationError('邮箱格式不正确')
        return attrs
    def update(self, instance, validated_data):
        instance.email=validated_data.get('email')
        instance.save()
        # 发送邮件

        url=generic_verify_url(instance.id)
        '''
        send_mail(subject,message,from_email,recipient_list,html_message=None)

        subject 邮件标题
        message 普通邮件正文， 普通字符串
        from_email 发件人
        recipient_list 收件人列表
        html_message 多媒体邮件正文，可以是html字符串
        '''
        # msg = '<a href="http://www.itcast.cn/subject/pythonzly/index.shtml" target="_blank">点击激活</a>'
        # send_mail('注册激活', '', settings.EMAIL_FROM, ['qq1102746402@163.com'], html_message=msg)
        fsyx.delay(instance.email,url)
        return instance

class YhLlXlh(serializers.Serializer):
    sku_id=serializers.IntegerField(label='商品编号',min_value=1,required=True)
    def validate(self, attrs):

        return attrs
    def create(self, validated_data):
        yh_id = self.context.get('request')
        yh_id=yh_id.user
        sku_id=validated_data.get('sku_id')
        r_c=get_redis_connection('yhlljl')
        # 移除已经存在的本记录
        r_c.lrem('history_%s' % yh_id, 0, sku_id)
        # 添加新的记录
        r_c.lpush('history_%s' % yh_id, sku_id)
        # 保存最多5条记录
        r_c.ltrim('history_%s' % yh_id, 0, 4)
        return validated_data
class addressxlh(serializers.ModelSerializer):
    class Meta:
        model=Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')


