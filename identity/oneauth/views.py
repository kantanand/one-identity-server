# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
def user_login(request):
    if request.method == 'GET':
        TITLE = 'Login'
        LOGIN_URL = settings.LOGIN_URL
        next_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        return render(request, 'login.html', locals())

@login_required
def user_logout(request):
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')