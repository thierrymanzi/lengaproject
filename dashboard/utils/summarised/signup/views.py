from threading import Thread

from django.db.models import Count, F

from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

import calendar
from datetime import datetime, timedelta, date
from django.core.cache import cache

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


class UserSignUpStatsView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_active=True)
        e = users.filter(first_name='elijahbarazatest').last()
        print("ELIJAH000={}".format(e))

        breakdown_by = request.query_params.get('breakdown', None)
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
        location = Location.objects.filter(is_active=True)

        if partner_ not in ['all', 'no_partner', 'all_partners_and_no_partner', None]:
            partner = partner.filter(
                id=partner_
            )

        no_partner_ids, no_partner_ids_list = get_no_partners()
        if partner_ in no_partner_ids_list:
            partner = 'no_partner'

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
        print("user_id={}".format(user_id))
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
        baseSignupStats = BaseSignupHandler(
                request, users, month_or_week, partner,
                location, user_type, start_date, end_date,
                breakdown_by
            )
        response = baseSignupStats.getSummaryStats()


        return Response(
            {'data': response},
            status=status.HTTP_200_OK
        )
