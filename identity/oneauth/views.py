# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
@csrf_exempt
def user_login(request):
    if request.method == 'GET':
        TITLE = 'Login'
        LOGIN_URL = settings.LOGIN_URL
        next_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        return render(request, 'login.html', locals())
    if request.method == 'POST':
        user_name = request.POST.get("username", None)
        user_pass = request.POST.get("password", None)
        print "user_name {}".format(user_name)
        print "user_pass {}".format(user_pass)
        if user_name and user_pass:
            user = authenticate(username=user_name, password=user_pass)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')

@login_required
def user_logout(request):
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')