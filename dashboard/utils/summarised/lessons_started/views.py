from threading import Thread

from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status

import calendar
from datetime import datetime, timedelta, date
from django.core.cache import cache

from dashboard.utils.summarised.lessons_started.lessons_started_handler import BaseLessonsStartedHandlerHandler
from dashboard.utils.summarised.engagement.engagement_handler import BaseEngagementHandler
from dashboard.utils.summarised.general_utils import get_no_partners
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


class LessonsStartedStatsView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_active=True)

        breakdown_by = request.query_params.get('breakdown', None)
        module_id = request.query_params.get('module', None)
        lesson_id = request.query_params.get('lesson', None)
        partner_ = request.query_params.get('partner', None)
        location_ = request.query_params.get('location', None)
        user_type_ = request.query_params.get('user_type', None)
        month_or_week = request.query_params.get('month_or_week', None)
        user_id = request.query_params.get('user_id', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date is None and end_date is None:
            start_date = request.query_params.get('start_date', '2020-11-01')
            end_date = request.query_params.get('end_date', str(datetime.now().date()))

        partner = Partner.objects.filter(is_active=True).exclude(
            name__icontains='test'
        )
        location = Location.objects.filter(is_active=True).exclude(
            name__icontains='test'
        )
        modules = Category.objects.all()
        lessons = []


        if partner_ not in ['all', 'no_partner', None,'all_partners_and_no_partner']:
            partner = partner.filter(
                id=partner_
            )
        no_partner_ids, no_partner_ids_list = get_no_partners()
        print("no_partner_ids={}".format(no_partner_ids))
        print("no_partner_ids_list={}".format(no_partner_ids_list))
        print("partner_={}".format(partner_))
        if partner_ in no_partner_ids_list:
            partner = 'no_partner'
        print("partner={}".format(partner))
        if location_ not in ['all', None]:
            location = location.filter(
                id=location_
            )
        if user_type_ not in ['all', None]:
            user_type = [user_type_.capitalize()]
        if user_type_ in ['all', None]:
            user_type = [choice.INDIVIDUAL, choice.GROUP]

        if user_id is not None:
            users = users.filter(
                id=user_id
            )
        breakdown_by = breakdown_by.lower()
        if breakdown_by == 'module':
            if module_id not in ['all', None]:
                modules = modules.filter(
                    id=module_id
                )
                lessons = Lesson.objects.filter(
                    category=modules.last()
                )
                if lesson_id not in ['all', None]:
                    lessons = lessons.filter(
                        id=lesson_id
                    )



        elif breakdown_by == 'lesson':
            if module_id not in ['all', None]:
                modules = modules.filter(
                    id=module_id
                )
            else:
                modules = modules.filter(order=1)

            lessons = Lesson.objects.filter(
                category=modules.last()
            )
            if lesson_id not in ['all', None]:
                lessons = lessons.filter(
                    id=lesson_id
                )
            else:
                lessons = lessons.filter(
                    category=modules.filter(
                        order=1
                    ).last()
                )

        if partner_ == 'no_partner':
            partner = 'no_partner'
        if partner_ == 'all_partners_and_no_partner':
            partner = 'all_partners_and_no_partner'
        if partner_ == 'all':
            partner = 'all'
        if EXCLUDE_TEST_USERS:
            users = users.exclude(
                username__icontains='test'
            ).exclude(first_name__in=TEST_USERS_LIST).exclude(
                created__date__lt=EXCLUDE_START_DATE
            )
        baseCompletionStats = BaseLessonsStartedHandlerHandler(
                request, users,
            month_or_week,
            partner,
            location, user_type, start_date, end_date,
            breakdown_by, modules, lessons
        )
        # baseEngagementStats.spendType = baseEngagementStats.SpendType.COMPLETED
        response = baseCompletionStats.getSummaryStats()


        return Response(
            {'data': response},
            status=status.HTTP_200_OK
        )
