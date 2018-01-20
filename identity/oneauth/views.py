# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
def user_login(request):
    return HttpResponse("login service")

@login_required
def user_logout(request):
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')