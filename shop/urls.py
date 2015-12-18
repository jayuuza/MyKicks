from django.conf.urls import include, url

from shop import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/(?P<product_id>[0-9]+)/$', views.detail, name='detail')
]