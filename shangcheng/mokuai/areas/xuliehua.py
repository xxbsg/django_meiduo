from  rest_framework import serializers

from areas.models import Area

#
# class ShangXlh(serializers.ModelSerializer):
#
#     class Meta:
#         model = Area
#         fields = ['name','id']
#
#
# class XiaXlh(serializers.ModelSerializer):
#     area_set=ShangXlh(many=True)
#     class Meta:
#         model = Area
#         fields = ['area_set']


class ShangXlh(serializers.ModelSerializer):


    class Meta:
        model = Area
        fields = ['id','name']


# 市
# class XiaXlh(serializers.ModelSerializer):
#
#     area_set = ShangXlh(many=True)
#
#     class Meta:
#         model = Area
#         fields = ['area_set','id','name']

class XiaXlh(serializers.ModelSerializer):

    # area_set = AreaSerializer(many=True)
    subs = ShangXlh(many=True)

    class Meta:
        model = Area
        # fields = ['area_set']
        fields = ['subs','id','name']