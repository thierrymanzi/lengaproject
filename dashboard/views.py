from threading import Thread

from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status

import calendar
from datetime import datetime, timedelta, date
from django.core.cache import cache

# from dashboard.filters import UsersAnalyticsFilter
from dashboard.utils.lessons_completion import BaseUptakeLessonCompletionStats
from dashboard.utils.progress.progress_base_stats import BaseProgressStats
from dashboard.utils.signup_stats import BaseUptakeStats

from dashboard.utils.modules_completion import BaseUptakeModuleCompletionStats
from dashboard.utils.usage.session_duration import BaseUsageStats
from utils.choices import Choice
from utils import view_mixins as generics
from users.models import User
from learning.models import Location, Lesson, Category
from utils.common import FileExport
from lenga.settings.local import EXCLUDE_TEST_USERS, TEST_USERS_LIST, EXCLUDE_START_DATE


class DashboardView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        users  = User.objects.filter(is_active=True)
        # users = users.exclude(username__icontains='test')
        locations = Lesson.objects.all()

        locations_details = [{
                    'name': location.name,
                    'users_count': users.filter(location=location).count(),
                    'modules_completion': location.modules_completion
                } for location in locations
                ]
        return Response({
            'users_count': users.count(),
            'locations': {
                'total_count': locations.count(),
                'locations_details': locations_details
            },
        }, status=status.HTTP_200_OK)


class UserSignUpStatsView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_active=True)
        user_id = request.query_params.get('user_id', "")
        if user_id != "":
            users = users.filter(id=user_id)
        # users = users.exclude(username__icontains='test').exclude(created__lte='2020-11-15')
        baseUptakeStats = BaseUptakeStats(request, users)
        # response = baseUptakeStats.getData()

        filter = request.build_absolute_uri()
        try:
            response = cache.get(filter)
            if response is None:
                response = baseUptakeStats.getData()
                cache.set(filter, response, 86400000)
        except Exception as e:
            cache.set(filter, response, 86400000)

        return Response(
            {'data': response},
            status=status.HTTP_200_OK
        )

class UserModuleCompletionStatsView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        modules = Category.objects.all()

        users = User.objects.filter(is_active=True)
        user_id = request.query_params.get('user_id', "")
        module_id = request.query_params.get('module', "")
        if user_id != "":
            users = users.filter(id=user_id)
        # users = users.exclude(username__icontains='test').exclude(created__lte='2020-11-15')
        # if module_id == "":
        #     modules = modules.filter(id="41a2a7b1-c2d0-4037-8e82-228c507aabb4")
        if module_id != '':
            modules = modules.filter(id=module_id)

        baseUptakeStats = BaseUptakeModuleCompletionStats(request, modules, users)
        # response = baseUptakeStats.getData()
        # filter = request.query_params.get('filter', None)
        # filter = request.build_absolute_uri()
        # try:
        #     response = cache.get(filter)
        #     if response is None:
        #         response = baseUptakeStats.getData()
        #         cache.set(filter, response, 86400000)
        # except Exception as e:
        #     cache.set(filter, response, 86400000)

        print("GOT HERE")
        response = baseUptakeStats.getData()


        return Response(
            {'data': response},
            status=status.HTTP_200_OK
        )


class UserLessonsCompletionStatsView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        modules = Category.objects.all()

        users = User.objects.filter(is_active=True)
        user_id = request.query_params.get('user_id', "")
        module_id = request.query_params.get('module', "")
        lesson_id = request.query_params.get('lesson_id', "")

        if user_id != "":
            users = users.filter(id=user_id)
        # users = users.exclude(username__icontains='test').exclude(created__lte='2020-11-15')
        if module_id == "":
            module = modules.filter(id="41a2a7b1-c2d0-4037-8e82-228c507aabb4").last()
        else:
            module = Category.objects.get(id=module_id)
        if lesson_id == "":
            lessons = Lesson.objects.filter(category=module)
        else:
            lessons = Lesson.objects.filter(id=lesson_id)

        baseUptakeStats = BaseUptakeLessonCompletionStats(request, lessons, users)
        # response = baseUptakeStats.getData()
        filter = request.build_absolute_uri()
        # try:
        #     response = cache.get(filter)
        #     if response is None:
        #         response = baseUptakeStats.getData()
        #         cache.set(filter, response, 86400000)
        # except Exception as e:
        #     cache.set(filter, response, 86400000)

        response = baseUptakeStats.getData()


        return Response(
            {'data': response},
            status=status.HTTP_200_OK
        )

class UsageSessionDurationStatsView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        modules = Category.objects.all()

        users = User.objects.filter(is_active=True)
        user_id = request.query_params.get('user_id', "")
        module_id = request.query_params.get('module_id', "")
        if user_id != "":
            users = users.filter(id=user_id)
        # users = users.exclude(username__icontains='test').exclude(created__lte='2020-11-15')
        if module_id != "":
            modules = modules.filter(id=module_id)

        baseUptakeStats = BaseUsageStats(request, modules, users)

        # filter = request.build_absolute_uri()
        # try:
        #     response = cache.get(filter)
        #     if response is None:
        #         response = baseUptakeStats.getData()
        #         cache.set(filter, response, 86400000)
        # except Exception as e:
        #     cache.set(filter, response, 86400000)

        response = baseUptakeStats.getData()

        return Response(
            {'data': response},
            status=status.HTTP_200_OK
        )


class ProgressStatsView(generics.ListAPIView):

    def getAppData(self):
        def send():
            self.baseProgressStats.getData()
        Thread(target=send).start()


    def get(self, request, *args, **kwargs):
        modules = Category.objects.all()

        users = User.objects.filter(is_active=True)
        user_id = request.query_params.get('user_id', "")
        if user_id != "":
            users = users.filter(id=user_id)
        if EXCLUDE_TEST_USERS:
            users = users.exclude(
                username__icontains='test'
            ).exclude(first_name__in=TEST_USERS_LIST).exclude(
                created__date__lt=EXCLUDE_START_DATE
            )
        # for user in users:

        # users = users.exclude(username__icontains='test').exclude(created__lte='2020-11-15')

        self.baseProgressStats = BaseProgressStats(request, modules, users)


        if filter == 'all_users_stats':
            self.getAppData()
            response = {'message': 'Export will be sent to your email'}
        else:
            # try:
            #     response = cache.get(filter)
            #     if response is None:
            #         response = self.baseProgressStats.getData()
            #         cache.set(filter, response, 86400000)
            # except Exception as e:
            #     cache.set(filter, response, 86400000)
            response = self.baseProgressStats.getData()

        return Response(
            {'data': response},
            status=status.HTTP_200_OK
        )

