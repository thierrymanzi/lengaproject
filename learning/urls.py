# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-06-15 14:42:43
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-06-15 15:14:55
# Project: lenga

from django.urls import path, re_path

from learning.api import views

urlpatterns = [
    # categories
    path('api/v1/categories/',
         views.ListCreateCategoryView.as_view()),
    re_path('api/v1/categories/(?P<id>[0-9a-z-]+)/',
            views.UpdateCategoryView.as_view()),

    # lessons
    path('api/v1/lessons/', views.ListCreateLessonView.as_view()),
    re_path('api/v1/lessons/(?P<id>[0-9a-z-]+)/',
            views.UpdateLessonView.as_view()),

    # questions
    path('api/v1/questions/',
         views.ListCreateQuestionView.as_view()),
    re_path('api/v1/questions/(?P<id>[0-9a-z-]+)/',
            views.UpdateQuestionView.as_view()),
    # question options
    path('api/v1/options/', views.ListCreateOptionView.as_view()),
    re_path('api/v1/options/(?P<id>[0-9a-z-]+)/',
            views.UpdateOptionView.as_view()),
    # question answers
    path('api/v1/answers/', views.ListCreateAnswerView.as_view()),
    re_path('api/v1/answers/(?P<id>[0-9a-z-]+)/',
            views.UpdateAnswerView.as_view()),
    # upload media files
    path('api/v1/learning/media/uploads/', views.UploadMediaFilesView.as_view(), name="upload_media_files"),
   #  work on a media file
    re_path('api/v1/learning/media/uploads/(?P<id>[0-9a-z-]+)/', views.UpdateMediaFileView.as_view(),
            name="update_media_file"),
    path('api/v1/learning/get_total_files/', views.GetUploadsCount.as_view(), name="get_total_files"),
    path('api/v1/learning/content-update-completed/', views.NotifyContentUpdateComplete.as_view(), name="content-update-completed"),
]
