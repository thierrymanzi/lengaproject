from rest_framework.response import Response

from utils import view_mixins as generics
from utils.common import FileExport
from .filters import (
    LessonTrackingFilter, QuestionTrackingFilter,
    CategoryTrackingFilter
)
from .serializers import (
    LessonTrackingSerializer, QuestionTrackingSerializer,
    CategoryTrackingSerializer
)
from ..models import (
    LesssonTracking, QuestionTracking,
    CategoryTracking
)


class ListCreateLessonsTrackingView(generics.ListCreateAPIView):
    queryset = LesssonTracking.objects.filter(is_active=True)
    serializer_class = LessonTrackingSerializer
    filter_class = LessonTrackingFilter


class UpdateLessonsTrackingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LesssonTracking.objects.filter(is_active=True)
    serializer_class = LessonTrackingSerializer
    lookup_field = 'id'


class ListCreateQuestionsTrackingView(generics.ListCreateAPIView):
    queryset = QuestionTracking.objects.filter(is_active=True)
    serializer_class = QuestionTrackingSerializer
    filter_class = QuestionTrackingFilter


class UpdateQuestionsTrackingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionTracking.objects.filter(is_active=True)
    serializer_class = QuestionTrackingSerializer
    lookup_field = 'id'


class ListCreateCategoriesTrackingView(generics.ListCreateAPIView):
    queryset = CategoryTracking.objects.filter(is_active=True)
    serializer_class = CategoryTrackingSerializer
    filter_class = CategoryTrackingFilter


class UpdateCategoriesTrackingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryTracking.objects.filter(is_active=True)
    serializer_class = CategoryTrackingSerializer
    lookup_field = 'id'


class ExportCategories(generics.ListAPIView):
    filter_class = CategoryTrackingFilter

    def get(self, request, *args, **kwargs):
        categories = self.filter_queryset(CategoryTracking.objects.all())
        res = []
        for category in categories:
            for data in category.data:
                res.append({
                    'start_time': data['start_time'],
                    'end_time': data['end_time'],
                    'category_name': category.category.name
                })

        handler = FileExport(res)
        return Response({'file_url': handler.file_export()})


class ExportLessons(generics.ListAPIView):
    filter_class = LessonTrackingFilter

    def get(self, request, *args, **kwargs):
        lessons = self.filter_queryset(LesssonTracking.objects.all())
        res = []
        for lesson in lessons:
            for data in lesson.data:
                res.append({
                    'start_time': data['start_time'],
                    'end_time': data['end_time'],
                    'lesson_category_name': lesson.lesson.category.name
                })

        handler = FileExport(res)
        return Response({'file_url': handler.file_export()})
