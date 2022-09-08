# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 11:14:03
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 14:00:41
# Project: lenga
from django.urls import path, re_path

from users.api.views import (
    ListUsers, RetrieveUpdateUsers, CurrentUserView,
    LoginUserView, UserRegistration, ExportUsers,
    ListPartners, ListLocations)

urlpatterns = [
    path(r'api/v1/users/current-user/',
         CurrentUserView.as_view(),
         name='current_user'),
    path(
        r'api/v1/users/login-user/',
        LoginUserView.as_view(),
        name='login_user'
    ),

    path(r'api/v1/users/', ListUsers.as_view()),
    path(r'api/v1/partners/', ListPartners.as_view()),
    path(r'api/v1/locations/', ListLocations.as_view()),
    path(r'api/v1/users/registration/', UserRegistration.as_view()),
    re_path(r'api/v1/users/(?P<id>[0-9a-z-]+)/', RetrieveUpdateUsers.as_view()),

    path(r'api/v1/exports/users/', ExportUsers.as_view()),

]
