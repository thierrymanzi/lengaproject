from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status


from datetime import datetime, timedelta, date

from dashboard.utils.summarised.general_utils import get_no_partners
from dashboard.utils.summarised.period_utils import PeriodUtils
from dashboard.utils.summarised.signup.breakdown_utils.all import getBreakdownByAll
from dashboard.utils.summarised.signup.breakdown_utils.location import getBreakdownByLocation
from dashboard.utils.summarised.signup.breakdown_utils.partners import getBreakdownByPartners
from dashboard.utils.summarised.signup.breakdown_utils.period import getBreakdownByPeriod
from dashboard.utils.summarised.signup.breakdown_utils.user_type import getBreakdownByUserType
from utils.choices import Choice as choice
from users.models import User
from learning.models import Location, Lesson, Partner


class BaseSignupHandler:
    def __init__(
            self, request, users, period_type, partners,
            locations, user_type, start_date, end_date,
            breakdown_item
    ):
        period_type = period_type if period_type is\
                                     not None else choice.MONTH
        period_type = period_type.capitalize()
        self.request = request
        self.users = users
        # self.period_type = period_type  #
        self.partners = partners
        self.locations = locations
        self.user_type = user_type
        self.start_date = start_date
        self.end_date = end_date
        self.period_details = PeriodUtils(
            period_type, start_date, end_date
        )
        self.breakdown_item = breakdown_item.capitalize()



    def get_queryset(self):
        """
        If any of the filters gets here as None,
        it means select all items in that filter/do
        not add the filter
        """

        # all_signups = self.users.filter(
        #     signup_date__gte=self.start_date,
        #     signup_date__lte=self.end_date,
        # )
        # e = self.users.filter(first_name='elijahbarazatest').last()
        all_signups = self.users.filter(
            created__date__gte=self.start_date,
            created__date__lte=self.end_date,
        )
        if self.partners:
            #If self.partners is not None, get here
            no_partners_ids, no_partners_ids_list = get_no_partners()
            if self.partners == 'no_partner':
                print("GOT HERE: NO PARTNER")
                no_partner = Partner.objects.filter(
                    is_active=True,
                    id__in=no_partners_ids_list
                )
                all_signups1 = all_signups.filter(
                    partner=None
                )
                all_signups = all_signups.filter(
                    partner__in=no_partner
                ) | all_signups1

                self.partners = no_partner
            else:
                if self.partners == 'all':
                    self.partners = Partner.objects.filter(
                        is_active=True
                    ).exclude(
                    id__in=no_partners_ids_list
                )
                    all_signups = all_signups.filter(
                        partner__in=self.partners
                    ).exclude(partner=None)
                elif self.partners == 'all_partners_and_no_partner':
                    pass
                else:
                    all_signups = all_signups.filter(
                        partner__in=self.partners
                    )
            # pass
        if self.locations:
            all_signups = all_signups.filter(
                location__in=self.locations
            )
        if self.user_type:
            all_signups = all_signups.filter(
                account_type__in=self.user_type
            )
        self.queryset = all_signups


    def getSummaryStats(self):
        print("DATA 0")

        response = []
        self.get_queryset()

        # print("self.period_details.period_type={}".format(self.period_details.period_type))
        if self.period_details.period_type == choice.MONTH:
            self.period_details.month_dates_in_period()
            dates_in_period = self.period_details.month_dates_in_period
            # print("dates_in_period1={}".format(dates_in_period))
        else:
            self.period_details.weeks_dates_in_period()
            dates_in_period = self.period_details.weeks_dates_in_period
            # print("dates_in_period2={}".format(dates_in_period))



        if self.breakdown_item in ['All']:
            print("DATA 1")
            response = getBreakdownByAll(self, response, choice)
        elif self.breakdown_item in [choice.PARTNER.capitalize()]: #, choice.MONTH, choice.WEEK]:
            print("DATA 2")
            response = getBreakdownByPartners(self, response, choice)
        elif self.breakdown_item in [choice.LOCATION.capitalize()]: #, choice.MONTH, choice.WEEK]:
            print("DATA 3")
            response = getBreakdownByLocation(self, response, choice)
        elif self.breakdown_item in [choice.USER_TYPE.capitalize()]:  # , choice.MONTH, choice.WEEK]:
            print("DATA 4")
            response = getBreakdownByUserType(self, response, choice)
        elif self.breakdown_item.capitalize() in [choice.PERIOD.capitalize()]:  # , choice.MONTH, choice.WEEK]:
            print("DATA 5")
            response = getBreakdownByPeriod(self, response, choice, dates_in_period, self.queryset, self.period_details.period_type)



        return response
