# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 20:51:03
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 21:06:54
# Project: lenga

from django.contrib import admin

from data_tracking.models import (
    QuestionTracking, LesssonTracking,
    CategoryTracking,LessonCompletionStats,
    ModuleQuestionsCompletedStats,
    UserCompletedModulesStats,
    CategoryTrackingStats,
    TimeTakenOnModuleStat,
    TimeTakenOnLessonStat,
    LessonsStartedStats,
    ModulesStartedStats
)

class CategoryTrackingAdmin(admin.ModelAdmin):
   list_display = ('category_order','category_name','user','data')
   ordering = ('category__order', 'user')

   def category_order(self, obj):
       return obj.category.order

   def category_name(self, obj):
       return obj.category.name



class LesssonTrackingAdmin(admin.ModelAdmin):
   list_display = ('category','lesson_order','lesson_name','user','data')

   def category(self, obj):
       return obj.lesson.category.order

   def lesson_order(self, obj):
       return obj.lesson.order

   def lesson_name(self, obj):
       return obj.lesson.description


class QuestionTrackingAdmin(admin.ModelAdmin):
   list_display = ('category','lesson_order','question_order','user','data')

   def category(self, obj):
       return obj.question.lesson.category.order

   def lesson_order(self, obj):
       return obj.question.lesson.order

   def question_order(self, obj):
       return obj.question.order

admin.site.register(CategoryTracking, CategoryTrackingAdmin)
admin.site.register(LesssonTracking, LesssonTrackingAdmin)
admin.site.register(QuestionTracking, QuestionTrackingAdmin)

#admin.site.register(QuestionTracking)
#admin.site.register(LesssonTracking)
#admin.site.register(CategoryTracking)
admin.site.register(LessonCompletionStats)
admin.site.register(ModuleQuestionsCompletedStats)
admin.site.register(UserCompletedModulesStats)
admin.site.register(CategoryTrackingStats)
admin.site.register(TimeTakenOnModuleStat)
admin.site.register(TimeTakenOnLessonStat)
admin.site.register(LessonsStartedStats)
admin.site.register(ModulesStartedStats)
