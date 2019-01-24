from django.conf.urls import url
from rest_framework import routers

from areas import views

urlpatterns = [
    # url(r"^infos/$",views.ShengFen.as_view()),
    # url(r"^infos/(?P<shang>\d{6})/$", views.ShiXian.as_view()),

]
router=routers.DefaultRouter()
router.register(r'infos',views.ChengShi,base_name='chengshi')
urlpatterns +=router.urls