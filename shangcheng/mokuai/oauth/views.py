# Create your views here.
from QQLoginTool.QQtool import OAuthQQ
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from oauth.models import QqYhb
from oauth.oa_gg import jopenid, jmopenid
from oauth.xuliehua import qqyhxlh
from shangcheng import settings


class Oauth(APIView):
    def get(self,requ):
        state = requ.query_params.get('state')
        if not state:
            state = 'text'

        # 获取QQ登录页面网址
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=state)
        login_url = oauth.get_qq_url()

        return Response({'auth_url': login_url})
class OauthGetOID(APIView):
    def get(self,requ):
        dat=requ.query_params
        code=dat.get('code')
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        token=oauth.get_access_token(code=code)
        openid=oauth.get_open_id(access_token=token)
        openid=jmopenid(openid)
        try:
            qyh=QqYhb.objects.get(openid=jopenid(openid))
        except:
            return Response({'access_token':openid})
        else:
            # 生成token字段返回
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(qyh.user)
            token = jwt_encode_handler(payload)

            return Response(
                {'token': token,
                 'username': qyh.user.username,
                 'user_id': qyh.user.id})

    def post(self,requ):
        # 获取 openid 手机号 密码 短信
        dat=requ.data
        openid = dat.get('access_token')
        openid=jopenid(openid)
        s=qqyhxlh(data=dat)
        s.is_valid(raise_exception=True)
        qyh=s.save()

        # 生成token字段返回
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(qyh.user)
        token = jwt_encode_handler(payload)

        return Response(
            {'token': token,
             'username': qyh.user.username,
             'user_id': qyh.user.id})
        # openid=dat.get('access_token')
        # openid=jopenid(openid)
        # yh=Yhb.objects.get(username='qwerq')
        #
        # return Response(data={'user_id':yh.id,'username':yh.username,'token':11111111})