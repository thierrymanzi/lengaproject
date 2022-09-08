from django_filters import rest_framework as filters

from ..models import (
    Category,
    Lesson,
    Question,
    QuestionOption,
    Answer,
    MediaFile
)


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name', 'order']


class LessonFilter(filters.FilterSet):
    class Meta:
        model = Lesson
        fields = ['category', 'order']


class QuestionFilter(filters.FilterSet):
    class Meta:
        model = Question
        fields = ['lesson', 'order', 'question_type']


class OptionFilter(filters.FilterSet):
    question = filters.CharFilter(
        field_name='options_qoptions__question', lookup_expr='exact', distinct=True)

    class Meta:
        model = QuestionOption
        fields = ['question']


class AnswerFilter(filters.FilterSet):
    class Meta:
        model = Answer
        fields = ['user', 'question']

class MediaFileFilter(filters.FilterSet):
    class Meta:
        model = MediaFile
        fields = ['id', 'file_name', 'created']