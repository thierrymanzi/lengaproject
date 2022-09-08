# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 11:49:05
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 11:52:35
# Project: lenga

from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from learning.api.viewsets import LocationViewSet

router = routers.DefaultRouter()

router.register(r'locations', LocationViewSet)

url_patterns = [
    path('api/v1/', include(router.urls)),
]
