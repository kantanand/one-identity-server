from django.conf.urls import url

from oneauth import views

urlpatterns = [
    url(r'^login/$', views.user_login),
    url(r'^logout/$', views.user_logout),
]