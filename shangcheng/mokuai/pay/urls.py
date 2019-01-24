from django.conf.urls import url

from pay import views

urlpatterns = [
    # orders/20190123090619000000007/
    url(r'^orders/(?P<orders_id>\d+)/$',views.pay.as_view()),
    ]