# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
class BlockChainTrasncations(models.Model):
    hash_record = models.TextField();
    transcation_type = models.CharField(max_length=100, default="GOVT");
    # Record Tracking
    created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True
