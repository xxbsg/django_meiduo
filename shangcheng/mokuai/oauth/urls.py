from django.conf.urls import url

from oauth import views

urlpatterns = [
    url(r'^qq/statues/$', views.Oauth.as_view()),
    url(r'^qq/users/$',views.OauthGetOID.as_view()),

]