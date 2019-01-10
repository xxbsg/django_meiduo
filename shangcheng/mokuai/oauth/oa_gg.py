from itsdangerous import TimedJSONWebSignatureSerializer as tjxlh
from shangcheng.settings import SECRET_KEY
def jmopenid(openid):
    s=tjxlh(secret_key=SECRET_KEY,expires_in=300)
    token=s.dumps({'openid':openid})
    return token.decode()
def jopenid(openid):
    s = tjxlh(secret_key=SECRET_KEY, expires_in=300)
    try:
        data1=s.loads(openid)
    except:
        token=None
    else:
        token=data1.get('openid')
    return token

