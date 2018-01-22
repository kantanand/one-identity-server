from django.conf.urls import url
from . import views
from rest_framework_jwt import views as vw 
from api import views as api

urlpatterns = [
    url(r'^get-auth-token/', vw.obtain_jwt_token),
    url(r'^get-auth-login/', api.auth_login),
    url(r'^auth-bc/', api.auth_bcn),
    url(r'^register/$', views.register),
    url(r'^set-user/$', api.set_user),
    url(r'^get-user/$', api.get_user),
]