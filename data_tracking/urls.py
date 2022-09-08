# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 21:08:16
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 21:08:16
# Project: lenga
from django.urls import path, re_path

from .api import views

urlpatterns = [
    re_path(r'api/v1/data-tracking/lessons/',
        views.ListCreateLessonsTrackingView.as_view()),
    re_path(r'api/v1/data-tracking/lessons/(?P<id>[0-9a-z-]+)/',
        views.UpdateLessonsTrackingView.as_view()),
    re_path(r'api/v1/data-tracking/questions/',
        views.ListCreateQuestionsTrackingView.as_view()),
    re_path(r'api/v1/data-tracking/questions/(?P<id>[0-9a-z-]+)/',
        views.UpdateQuestionsTrackingView.as_view()),
    path('api/v1/data-tracking/categories/', views.ListCreateCategoriesTrackingView.as_view()),
    re_path('api/v1/data-tracking/categories/(?P<id>[0-9a-z-]+)/',
         views.UpdateCategoriesTrackingView.as_view()),
    path(r'api/v1/exports/categories/', views.ExportCategories.as_view()),
    path(r'api/v1/exports/lessons/', views.ExportLessons.as_view()),
]
