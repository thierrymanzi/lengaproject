# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 11:20:16
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 11:20:18
# Project: lenga

from django_filters import rest_framework as filters

from users.models import User


class UserFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'account_type', 'is_staff', 'is_active', 'location']
