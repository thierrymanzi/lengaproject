# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-06-09 08:39:33
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-06-15 16:02:38
# Project: lenga

import inspect, os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_boto.s3.storage import S3Storage
from model_utils.models import TimeStampedModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from users.models import User
from utils.choices import (
    QUESTION_TYPES, RANK_TYPES, NORMAL_RANK,
    SHOW_QUESTION_OPTION_AUDIO_ICON_OPTIONS,
    SHOW_QUESTION_OPTION_AUDIO_ICON_NO,
    RANK_MOVABLE_ITEMS, QUESTION_OPTION,
    EFFECT_QUESTION_VALIDATION_CHOICES,
    EFFECT_QUESTION_VALIDATION_YES
)
from utils.common import BaseModel
from utils.const import *

s3 = S3Storage()
FILE_DIR = os.path.join(PARENT_DIR, 'data/media')

class LearningBaseModel(BaseModel):
    audio_file = models.URLField(max_length=400, default='', blank=True)
    order = models.PositiveIntegerField()
    description = models.TextField(default='')

    class Meta(BaseModel.Meta):
        abstract = True
        ordering = ['order']


class Category(LearningBaseModel):
    name = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=400, default='')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s: %s' % (self.name, self.description)


class Lesson(LearningBaseModel):
    thumbnail = models.URLField(max_length=400, default='')
    category = models.ForeignKey(
        Category, related_name='category_lessons',
        on_delete=models.PROTECT
    )
    header_color = models.CharField(max_length=1000, default='', null=True, blank=True)
    main_color = models.CharField(max_length=1000, default='', null=True, blank=True)
    footer_color = models.CharField(max_length=1000, default='', null=True, blank=True)
    tile_color = models.CharField(max_length=1000, default='', null=True, blank=True)

    def __str__(self):
        return self.description


class Question(LearningBaseModel):
    text = models.CharField(max_length=255, default='')
    # default through table is okay
    question_options = models.ManyToManyField(
        'learning.QuestionOption', blank=True
    )
    question_type = models.CharField(
        max_length=255, choices=QUESTION_TYPES, default='text')
    lesson = models.ForeignKey(
        Lesson, related_name='lesson_questions',
        on_delete=models.PROTECT
    )
    video_file = models.URLField(max_length=400, blank=True, null=True)
    # If it is a question of type rank, priority can be NORMAL OR PRIORITY_LIST
    rank_type = models.CharField(
        max_length=255, choices=RANK_TYPES, default=NORMAL_RANK, null=True)
    movable_rank_item = models.CharField(
        max_length=255, choices=RANK_MOVABLE_ITEMS, default=QUESTION_OPTION, null=True)
    is_active = models.BooleanField(default=True)
    thumbnail = models.URLField(max_length=400, default='', null=True, blank=True)
    description2 = models.CharField(max_length=255, default='', null=True, blank=True)
    effect_validation = models.CharField(
        max_length=255,
        choices=EFFECT_QUESTION_VALIDATION_CHOICES,
        default=EFFECT_QUESTION_VALIDATION_YES,
        null=True
    )


    def __str__(self):
        return self.description


class Answer(BaseModel):
    user = models.ForeignKey(
        User, related_name='user_answers',
        on_delete=models.PROTECT
    )
    question = models.ForeignKey(
        Question, related_name='question_answers',
        on_delete=models.PROTECT
    )
    answer = models.CharField(max_length=45, default='')

    def __str__(self):
        return "%s: %s" % (str(self.question), self.answer)


class QuestionOption(BaseModel):
    text = models.CharField(max_length=255, default='')
    thumbnail = models.URLField(max_length=400, default='', null=True)
    audio_file = models.URLField(max_length=400, default='', null=True)
    is_answer = models.BooleanField(default=False)
    sub_options = models.ManyToManyField('learning.QuestionOption', blank=True)
    order = models.PositiveIntegerField(default=0)
    show_audio_icon = models.CharField(
        max_length=255, choices=SHOW_QUESTION_OPTION_AUDIO_ICON_OPTIONS,
        default=SHOW_QUESTION_OPTION_AUDIO_ICON_NO,
        null=True
    )
    text_value = models.CharField(max_length=255, default='', null=True)
    associated_rank_priority_order = models.PositiveIntegerField(default=0, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text

class RankPriorityOption(BaseModel):
    """
    For drag and drop questions, there are questions that have a priority defined
    and to be displayed at the bottom of the app:
    E.g 1,2,3,4,5,6. This model stores these priorities so as to be attached to
     ranking questions
    """
    order = models.PositiveIntegerField(default=0)
    thumbnail = models.URLField(max_length=400, default='', null=True)
    question = models.ForeignKey(
        Question, related_name='rank_priority_option',
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.order)



class QuestionEndScreenAudio(BaseModel):
    audio_file = models.URLField(max_length=400, default='', blank=True)
    question = models.ForeignKey(
        Question, related_name='question_end_screen_audio',
        on_delete=models.PROTECT,
        null=True,
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ['order']



# class QuestionHasQuestionOptions(BaseModel):
#     question = models.ForeignKey(
#         Question, related_name='question_qoptions',
#         on_delete=models.PROTECT
#     )
#     options = models.ForeignKey(
#         QuestionOption, related_name='options_qoptions',
#         on_delete=models.PROTECT
#     )

#     def __str__(self):
#         return str(self.options)


class VideoSession(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, blank=False)
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    question = models.ForeignKey(
        Question, blank=False, on_delete=models.PROTECT)
    elapsedTime = models.DateTimeField(null=True)
    bufferedPosition = models.CharField(max_length=255)
    duration = models.DateTimeField(null=True)
    volume = models.IntegerField()
    eventType = models.CharField(max_length=255)
    finished = models.DateTimeField()
    videoStartTime = models.DateTimeField()
    videoEndTime = models.DateTimeField()


class Location(BaseModel):
    ''' Different locations in Rwanda '''
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Partner(BaseModel):
    name = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MediaFile(TimeStampedModel):

    '''
        upload media files to AWS bucket
    '''

    def get_upload_path(instance, filename):
        return "{}/{}".format(instance.file_name, instance.created)

    file_name = models.CharField(max_length=255, null=False)
    file_path = models.FileField(blank=False, null=False, upload_to=get_upload_path, max_length=400)
    file_description = models.TextField(default='', null=True)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "{} {}".format(self.file_name, self.file_description)

    def __str__(self):
        return "{}".format(self.file_name)


class ContentUpdatesTracker(BaseModel):
    item_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='item_ct')
    item_object_id = models.UUIDField()
    updated_item = GenericForeignKey('item_content_type', 'item_object_id')
    user = models.ForeignKey(
        User, related_name='content_updated_stats', on_delete=models.PROTECT)
    updated_on_device = models.BooleanField(default=True)

#Track all updates in all content
@receiver(post_save, sender=Category)
def save_update_category(sender, instance, **kwargs):
        track_update(instance)

@receiver(post_save, sender=Lesson)
def save_update_lesson(sender, instance, **kwargs):
        track_update(instance)

@receiver(post_save, sender=Question)
def save_update_question(sender, instance, **kwargs):
        track_update(instance)

@receiver(post_save, sender=QuestionOption)
def save_update_qo(sender, instance, **kwargs):
        track_update(instance)


@receiver(post_save, sender=RankPriorityOption)
def save_update_rpo(sender, instance, **kwargs):
        track_update(instance)


@receiver(post_save, sender=QuestionEndScreenAudio)
def save_update_qea(sender, instance, **kwargs):
        track_update(instance)


def track_update(item):
    print("Got to track")
    users = User.objects.filter(is_active=True)
    for user in users:
        ContentUpdatesTracker.objects.create(
            item_content_type=ContentType.objects.get_for_model(type(item)),
            item_object_id=item.id,
            updated_item=item,
            user = user,
            updated_on_device = False
        )

