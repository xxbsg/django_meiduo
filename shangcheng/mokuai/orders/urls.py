from django.conf.urls import url

from orders import views

urlpatterns = [
# http://api.meiduo.site:8000/orders/places/
    url(r"^places/$",views.select_goods.as_view()),
    url(r"^$",views.OrderView.as_view()),
    ]