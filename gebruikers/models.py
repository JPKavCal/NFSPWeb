# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserCompanyInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Company Details
    company_name = models.CharField(blank=False, max_length=50)
    company_website = models.URLField(blank=True)
    company_street_number = models.IntegerField()
    company_street_name = models.CharField(max_length=50)
    company_city = models.CharField(max_length=50)
    company_province = models.CharField(max_length=50)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
