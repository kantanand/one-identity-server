from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^adminportal/', views.adminportal),
    url(r'^userportal/', views.userportal),
    url(r'^agencyportal/', views.agencyportal),
]