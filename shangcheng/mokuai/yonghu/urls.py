from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token

from yonghu import views

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.YhmYz.as_view()),
    url(r'^$',views.YhZc.as_view()),
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$',views.YhmMobile.as_view()),
    # url(r'^auths/', obtain_jwt_token, name='auths'),
    #JWT扩展的登录视图，在收到用户名与密码时，
    # 也是调用Django的认证系统中提供的authenticate()来检查用户名与密码是否正确。
    url(r'auths/', obtain_jwt_token, name='auths'),

]
