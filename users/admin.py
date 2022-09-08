# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 13:02:16
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 13:11:08
# Project: lenga


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext, gettext_lazy as _  # noqa

from users.models import User


class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'username', 'first_name', 'last_name', 'is_staff', 'account_type', 'location'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', )
    search_fields = ('username', 'universe',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1', 'password2'
            ),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
         'fields': ('first_name', 'last_name', 'no_of_users', 'account_type','location')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Device info'), {'fields': ('geo_location', 'fcm_key',)}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Permission)
