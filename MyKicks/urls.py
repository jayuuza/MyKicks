from django.conf.urls import include, url
from django.contrib import admin



urlpatterns = [
    url(r'', include('shop.urls', namespace='shop')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^admin/', include(admin.site.urls)),
]
