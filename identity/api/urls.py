from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^set-user/$', 'api.views.set_user'),
    url(r'^get-user/$', 'api.views.get_user'),
]