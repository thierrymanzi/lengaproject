# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-06-15 14:42:43
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-06-15 15:52:49
# Project: lenga

from django.db import transaction
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from learning.api.serializers import (
    CategorySerializer,
    LessonSerializer,
    QuestionSerializer,
    QuestionOptionSerializer,
    AnswerSerializer, MediaFileSerializer,
    ListQuestionOptionSerializer)

from utils import view_mixins as generics
from .filters import (
    CategoryFilter,
    LessonFilter,
    QuestionFilter,
    OptionFilter,
    AnswerFilter, MediaFileFilter
)
from ..models import (
    Category,
    Lesson,
    Question,
    QuestionOption,
    # QuestionHasQuestionOptions,
    Answer, MediaFile,
    ContentUpdatesTracker)
from learning.utils.get_uploads_count import getCount


class ListCreateCategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_class = CategoryFilter



class UpdateCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ListCreateLessonView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_class = LessonFilter



class UpdateLessonView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'id'


class ListCreateQuestionView(generics.ListCreateAPIView):
    queryset = Question.objects.filter(is_active=True)#.all()
    serializer_class = QuestionSerializer
    filter_class = QuestionFilter



class UpdateQuestionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.filter(is_active=True) #all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


def _add_sub_options(option, sub_options):
    if sub_options:
        option.sub_options.add(*sub_options)


class ListCreateOptionView(generics.ListCreateAPIView):
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer
    filter_class = OptionFilter


    def perform_create(self, serializer):
        audio_file = self.kwargs.get('audio_file')
        
        option = serializer.save()
        try:
            question = Question.objects.get(id=self.request.data.get('question_id'))
            question.question_options.add(option)
            question.save()
        except Exception as e:
            pass
        _add_sub_options(option, self.request.data.get('sub_options'))


class UpdateOptionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer
    lookup_field = 'id'

    @transaction.atomic
    def perform_update(self, serializer):
        obj = serializer.save()
        _add_sub_options(obj, self.request.data.get('sub_options'))

    def perform_destroy(self, instance):
        option = self.request.data.get('sub_options')

        if option:
            # Disassociate sub_options from options
            instance.sub_options.remove(*option)
        super().perform_destroy(instance)


class ListCreateAnswerView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_class = AnswerFilter



class UpdateAnswerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'id'


class UploadMediaFilesView(generics.ListCreateAPIView):
    """
    Allow users to upload files
    """
    queryset = MediaFile.objects.filter(is_deleted=False)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = MediaFileSerializer
    filter_class = MediaFileFilter


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = self.request.data
        file_data = self.request.FILES.getlist('file_path')
        file_desc = data.get('file_description')
        files = []

        for f in file_data:
            file_name = "{}".format(f)
            try:
                upload = dict(
                    file_name=file_name,
                    file_description=file_desc,
                    file_path=f
                )
                files.append(upload)
            except Exception as e:
                pass

        serializer = MediaFileSerializer(data=files, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaFileListView(generics.ListAPIView):
    """list media files uploaded"""

    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    filter_backends = MediaFileFilter


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MediaFileSerializer(queryset, many=True)
        return Response(data=serializer.data)


class UpdateMediaFileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update particular media file
    """
    serializer_class = MediaFileSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # ONLY retrieve an attachment that is not marked as deleted
        return MediaFile.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted'])


class GetUploadsCount(generics.ListAPIView):
    """list media files uploaded"""

    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    filter_backends = MediaFileFilter


    def get(self, request):
        updates = ContentUpdatesTracker.objects.filter(
            user=self.request.user,
            updated_on_device=False
        ).count()

        return Response({
            'count': getCount(),
            'has_updates': 'YES' if updates > 0 else 'NO'
        }, status=200)


class NotifyContentUpdateComplete(generics.ListAPIView):
    """list media files uploaded"""

    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    filter_backends = MediaFileFilter


    def get(self, request):
        updates = ContentUpdatesTracker.objects.filter(
            user=self.request.user,
            updated_on_device=False
        )
        for update in updates:
            update.updated_on_device = True
            update.save()

        return Response({'message': "OK",}, status=200)
