
from django.conf.urls import url
from . import views

# http://127.0.0.1:8000/v1/commodity/sort/mobile?brand=vivo
urlpatterns = [
    url(r'^$',views.commodity),
    url(r'^/sort/(?P<com_sort>\w+)',views.commodity_sort),
    url(r'^/search$',views.commodity_search)
]
