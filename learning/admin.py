# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 20:51:03
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 21:05:43
# Project: lenga
from django.contrib import admin

from learning.models import (
    Answer, Category, Lesson,
    Question, QuestionOption, VideoSession,
    Location, MediaFile,
    RankPriorityOption,
    ContentUpdatesTracker,
    Partner
)

admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(Question)

admin.site.register(VideoSession)
# admin.site.register(QuestionTracking)
# admin.site.register(DataTracking)
admin.site.register(Answer)
admin.site.register(QuestionOption)
admin.site.register(RankPriorityOption)
admin.site.register(MediaFile)
admin.site.register(Location)
admin.site.register(ContentUpdatesTracker)
admin.site.register(Partner)

