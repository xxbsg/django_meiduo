import json

from rest_framework import serializers
from django_redis import get_redis_connection
from goods.models import SKU


class GwcXlh(serializers.Serializer):
    sku_id=serializers.IntegerField(required=True)
    count=serializers.IntegerField(required=True)
    selected=serializers.BooleanField(default=True,required=False)

    def validate(self, attrs):
        sku_id=attrs.get('sku_id')
        count=attrs.get('count')

        try:
            sku=SKU.objects.get(pk=sku_id)
        except:
            raise serializers.ValidationError('没有这个山品')
        if sku.stock < count:
            raise serializers.ValidationError('库存不足')
        return attrs
    def create(self, validated_data):
        yh=validated_data.get('yh')
        nsku_id = validated_data.get('sku_id')
        ncount = validated_data.get('count')
        nselected = validated_data.get('selected')

        r_c=get_redis_connection('gwc')
        jl=r_c.get(yh)
        if jl is not None:
            globals = {
                'true': True
            }
            dic=eval(jl.decode(),globals)
            if str(nsku_id) in dic:
                dic[str(nsku_id)]['count']+=ncount
                validated_data['count']= dic[str(nsku_id)]['count']
                dic[str(nsku_id)]['selected']=nselected
            else:
                dic[nsku_id]={'count':ncount,'selected':nselected}

        else:
            dic = {str(nsku_id): {'count': ncount, 'selected': nselected}}
        s_dic = json.dumps(dic)
        r_c.set(yh,s_dic)
        return validated_data

class GwclbXlh(serializers.ModelSerializer):
    count = serializers.IntegerField(required=True)
    selected = serializers.BooleanField(default=True, required=False)
    class Meta:
        model=SKU
        fields = ('id', 'name', 'price', 'default_image_url', 'comments','count','selected')
    def update(self, instance, validated_data):
        pass