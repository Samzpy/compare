
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^/register$',views.user_register),
    url(r'^/login$',views.user_login),
    url(r'^$',views.check_token),
]
