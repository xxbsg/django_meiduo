import re
from django.contrib.auth.backends import ModelBackend

from yonghu.models import Yhb


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


class UsernameMobleModelBackend(ModelBackend):
    def authenticate(self,request, username=None, password=None, **kwargs):
        try:
            if re.match(r'1[3-9]\d{9}',username):
                yh=Yhb.objects.get(mobile=username)
            else:
                yh=Yhb.objects.get(username=username)
        except Yhb.DoesNotExist:
            yh=None
        if yh is not None:
            a=yh.check_password(password)
            if a:
                return yh