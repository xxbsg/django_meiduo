from django.conf.urls import url

from goods import views

urlpatterns = [
    # http://api.meiduo.site:8000/goods/categories/115/hotskus/
    # url(r'^rexiao/(?P<leiid>\d+)/$',views.ReXiao.as_view()),
    url(r'^categories/(?P<leiid>\d+)/hotskus/',views.ReXiao.as_view()),
    # categories/115/skus/?page=1&page_size=5&ordering=-create_time
    url(r'^categories/(?P<leiid>\d+)/skus/$',views.Splb.as_view()),
]
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('search', views.SKUSearchViewSet, base_name='skus_search')

urlpatterns += router.urls