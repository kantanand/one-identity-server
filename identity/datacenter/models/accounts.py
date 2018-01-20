# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # Record Tracking
    created_by = models.CharField(max_length=250, blank=True)
    created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)
    # Block Details ==============================
    account_address = models.TextField(null=True, blank=True)
    # User Roles
    is_admin     = models.BooleanField(default=0)
    is_member    = models.BooleanField(default=0)
    is_agency 	 = models.BooleanField(default=0)

    class Meta:
        app_label = 'datacenter'
        managed = True

    # override the unicode method to return the username on this model
    def __unicode__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    post_save.connect(create_user_profile, sender=User)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
