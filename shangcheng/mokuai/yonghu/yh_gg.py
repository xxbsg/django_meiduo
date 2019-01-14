# from itsdangerous import TimedJSONWebSignatureSerializer as tjxlh
# from shangcheng.settings import SECRET_KEY
# def jiami_e_id(id):
#     s=tjxlh(secret_key=SECRET_KEY,expires_in=300)
#     token=s.dumps({'token':id})
#     return 'http://www.meiduo.site:8080/success_verify_email.html?token='+token.decode()
# def jiemi_e_id(id):
#     s = tjxlh(secret_key=SECRET_KEY, expires_in=300)
#     try:
#         data1 = s.loads(id)
#     except:
#         token = None
#     else:
#         token = data1.get('token')
#     return token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature

from shangcheng import settings


def generic_verify_url(user_id):


    # 1. 创建序列化器
    s = Serializer(secret_key=settings.SECRET_KEY,expires_in=3600)
    #2. 组织数据
    data = {
        'id':user_id
    }
    #3. 对数据加密
    token = s.dumps(data)
    #4. 拼接url

    return 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token.decode()


def check_token(token):

    #1. 创建序列化器
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
    #2. 解析数据
    try:
        result = s.loads(token)
    #     b'eyJleHAiOjE1NDc0NjczMDYsImlhdCI6MTU0NzQ2MzcwNiwiYWxnIjoiSFMyNTYifQ.eyJpZCI6N30.8ebmjZJvPxbXd_S4y5rEJ38uhHCauWa7za29FT5YQEw'
    except BadSignature:
        return None

    #3.返回user_id
    return result.get('id')



