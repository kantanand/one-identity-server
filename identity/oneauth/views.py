# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return HttpResponse("login service")

# Create your views here.
def logout(request):
    return HttpResponse("logout service")