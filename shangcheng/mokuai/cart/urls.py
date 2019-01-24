from django.conf.urls import url

from cart import views

urlpatterns = [
    url(r'^$',views.carts.as_view())
]