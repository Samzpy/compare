from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.com_detail),
    url(r'^/track$',views.com_detail),
]
