from django_filters import rest_framework as filters

from ..models import (LesssonTracking, QuestionTracking,
                      CategoryTracking
                      )


class LessonTrackingFilter(filters.FilterSet):
    class Meta:
        model = LesssonTracking
        fields = ['lesson', 'user', 'is_active']


class QuestionTrackingFilter(filters.FilterSet):
    class Meta:
        model = QuestionTracking
        fields = ['question', 'user', 'is_active']

class CategoryTrackingFilter(filters.FilterSet):
    class Meta:
        model = CategoryTracking
        fields = ['category', 'user', 'is_active']
