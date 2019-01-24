import base64
import json
import pickle
from django_redis import get_redis_connection

from cart.xuliehua import GwcXlh


def hebing(request,user,response):
    cart_str = request.COOKIES.get('cart')
    if cart_str is not None:
        c_cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
        # s=GwcXlh(data=c_cart_dict)
        # s.is_valid(raise_exception=True)
        # c_cart_dict=s.data

        r_c=get_redis_connection('gwc')
        r_dict_str=r_c.get((user.id))
        if r_dict_str is not None:
            r_cart_dict=(r_dict_str).decode()
        else:
            r_cart_dict=str({})
        globals = {
            'true': True
        }
        r_cart_dict=eval(r_cart_dict,globals)
        for c_dict in c_cart_dict.keys():
            r_cart_dict[str(c_dict)]={'count':c_cart_dict[c_dict]['count'],'selected': c_cart_dict[c_dict]['selected']}


        r_c.set(str(user.id),json.dumps(r_cart_dict))

    return response
