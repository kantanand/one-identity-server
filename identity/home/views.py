# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html', locals())

@login_required
def adminportal(request):
    return render(request, 'adminportal.html', locals())

@login_required
def userportal(request):
    return render(request, 'userportal.html', locals())

@login_required
def agencyportal(request):
    return render(request, 'agencyportal.html', locals())