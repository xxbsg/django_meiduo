from django.conf.urls import url, include

from yanzheng import views

urlpatterns = [
    url(r'imagecodes/(?P<image_code_id>.+)/$',views.Yzm.as_view()),
    url(r'smscodes/(?P<mobile>1[345789]\d{9})/$',views.SjYzm.as_view())

]