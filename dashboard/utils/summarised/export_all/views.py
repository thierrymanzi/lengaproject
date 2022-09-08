from threading import Thread

from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status

import calendar
from datetime import datetime, timedelta, date
from django.core.cache import cache

from dashboard.utils.summarised.engagement.engagement_handler import BaseEngagementHandler
from dashboard.utils.summarised.export_all.export_handler import BaseExportAllHandler
from lenga.settings.local import EXCLUDE_TEST_USERS, TEST_USERS_LIST, EXCLUDE_START_DATE
from utils.choices import Choice as choice

# from dashboard.filters import UsersAnalyticsFilter
from dashboard.utils.lessons_completion import BaseUptakeLessonCompletionStats
from dashboard.utils.progress.progress_base_stats import BaseProgressStats
from dashboard.utils.signup_stats import BaseUptakeStats

from dashboard.utils.modules_completion import BaseUptakeModuleCompletionStats
from dashboard.utils.summarised.signup.signup_handler import BaseSignupHandler
from dashboard.utils.usage.session_duration import BaseUsageStats
from utils.choices import Choice
from utils import view_mixins as generics
from users.models import User
from learning.models import Location, Lesson, Category, Partner
from utils.common import FileExport



class ExportAllStatsView(generics.ListAPIView):

    def getAppData(self):
        def send():
            print("GOT HERE 3")
            self.baseExportAllHandler.getSummaryStats()
        Thread(target=send).start()

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_active=True)

        emailTo = request.query_params.get('email', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date is None and end_date is None:
            start_date = request.query_params.get('start_date', '2020-11-01')
            end_date = request.query_params.get('end_date', str(datetime.now().date()))
        if start_date == '2020-09-01':
            start_date = EXCLUDE_START_DATE


        modules = Category.objects.all()
        lessons = Lesson.objects.all()



        if EXCLUDE_TEST_USERS:
            users = users.exclude(
                username__icontains='test'
            ).exclude(first_name__in=TEST_USERS_LIST).exclude(
                created__date__lt=EXCLUDE_START_DATE
            )
        # baseExportAllHandler = BaseExportAllHandler(
        #     request, users, start_date, end_date,
        #     modules, lessons, emailTo
        # )

        print("GOT HERE 1")

        self.baseExportAllHandler = BaseExportAllHandler(
            request, users, start_date, end_date,
            modules, lessons, emailTo
        )
        print("GOT HERE 2")


        self.getAppData()
        response = {'message': 'Export will be sent to your email'}

        return Response(
            {'data': response},
            status=status.HTTP_200_OK
        )