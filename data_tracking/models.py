from django.contrib.postgres.fields import JSONField
from django.db import models

from learning.models import Lesson, Question, Category
from users.models import User
from utils.common import BaseModel



class LesssonTracking(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    data = JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        User, related_name='lesson_tracking', on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.lesson, self.user)
    class Meta:
        ordering = ['-created']


class QuestionTracking(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    data = JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        User, related_name='question_tracking', on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.question, self.user)
    class Meta:
        ordering = ['-created']

class CategoryTracking(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    data = JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        User, related_name='category_tracking', on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.category, self.user)
    class Meta:
        ordering = ['-created']


class LessonCompletionStats(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, related_name='lesson_completed', on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.FloatField(default=0.0)


class LessonsStartedStats(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, related_name='lesson_started_user', on_delete=models.PROTECT)
    start_date = models.DateTimeField()

class ModulesStartedStats(BaseModel):
    module = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, related_name='module_started_user', on_delete=models.PROTECT)
    start_date = models.DateTimeField()


class ModuleQuestionsCompletedStats(BaseModel):
    module = models.ForeignKey(Category, on_delete=models.PROTECT)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, related_name='lesson_question_completed', on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    completion_date = models.DateTimeField()
    total_items_in_module = models.FloatField(default=0.0)


class UserCompletedModulesStats(BaseModel):
    module = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, related_name='modules_completed', on_delete=models.PROTECT)
    start_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    duration = models.FloatField(default=0.0)



class CategoryTrackingStats(BaseModel):
    module = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, related_name='modules_completed_stat', on_delete=models.PROTECT)
    start_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)


class TimeTakenOnModuleStat(BaseModel):
    module = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, related_name='user_checking_module',
        on_delete=models.PROTECT
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.FloatField(default=0.0)


class TimeTakenOnLessonStat(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, related_name='user_checking_lesson',
        on_delete=models.PROTECT
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.FloatField(default=0.0)



