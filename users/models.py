# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 11:14:03
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 11:39:19
# Project: lenga

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token

from utils.choices import Choice
from utils.common import BaseModel
from .manager import UserManager


class Permissions(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150)

    def __str__(self):
        return '%s: %s' % (self.name, self.description)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    objects = UserManager()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=5000, unique=True)
    is_active = models.BooleanField(default=True)
    geo_location = JSONField(default=dict, blank=True)
    no_of_users = models.PositiveIntegerField(default=1)
    is_staff = models.BooleanField(default=True)
    permission = models.ManyToManyField(
        Permissions, related_name='user_permission', blank=True)
    app_version = models.CharField(max_length=10, default='')
    account_type = models.CharField(
        max_length=20,
        choices=Choice.ACCOUNT_TYPE,
        default=Choice.INDIVIDUAL
    )
    location = models.ForeignKey(
        'learning.Location',
        on_delete=models.CASCADE,
        blank=True, null=True
        )
    partner = models.ForeignKey(
        'learning.Partner',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    # profile information
    phone_number = PhoneNumberField(blank=True)
    # firebase key
    fcm_key = models.CharField(max_length=255, blank=True, null=True)
    signup_date = models.DateField(null=True,blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_full_name(self):
        return str(self)

    def all_permissions(self):
        return [perm.name for perm in self.permission.all()]


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
