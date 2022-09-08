from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status

import calendar
from datetime import datetime, timedelta, date
from utils.choices import Choice
from users.models import User
from learning.models import Location, Lesson

class BaseUptakeStats:
    def __init__(self, request, users):
        self.request = request
        self.users = users

    def get_weeks_dates_in_period(self, start_date, end_date):
        start_date = datetime.strptime(start_date,"%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        weeks = []
        days_diff = (end_date - start_date).days
        curr_date = start_date
        for k in range(0, days_diff + 1):
            curr_date = curr_date + timedelta(days=1)
            if curr_date.weekday() == 0:
                weeks.append(
                    {
                        'start_date': curr_date,
                        'end_date': curr_date + timedelta(days=6)
                    }
                )
        return weeks

    def get_month_dates_in_period(self, start_date, end_date):
        start_date = datetime.strptime(start_date,"%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")


        num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

        months = []
        curr_date = start_date
        for k in range(0, num_months + 1):
            days_in_curr_month = calendar.monthrange(
                curr_date.year, curr_date.month
            )[1]

            curr_date_end_date = curr_date + timedelta(days=days_in_curr_month)


            months.append(
                {
                    'start_date': date(curr_date.year, curr_date.month, 1),
                    # 'end_date': curr_date_end_date, #curr_date + timedelta(days=days_in_curr_month-1)
                    'month_date': curr_date_end_date - timedelta(days=1),
                    'end_date': curr_date_end_date - timedelta(days=1),
                }
            )
            curr_date = curr_date_end_date
        return months

    def getStartDate(self, week, month_or_week):
        start_date = None
        try:
            start_date_ = week['start_date'].date()
        except Exception as e:
            start_date_ = week['start_date']
        try:
            month_date = week['month_date'].date()
        except Exception as e:
            pass
        start_date = start_date_
        start_date_ = start_date_ if month_or_week != 'month' else month_date

        return start_date, start_date_, week['end_date']



    def getData(self):
        #Total number of people who have signed up
        #Location of users
        #Type of User
        #Location of users
        request = self.request
        users = self.users

        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        user_account_type = request.query_params.get('user_account_type', None)
        location = request.query_params.get('location', None)

        response  = []


        total_users = request.query_params.get('total_users', None)
        month_or_week = request.query_params.get('month_or_week', None)

        if start_date is None and end_date is None:
            start_date = request.query_params.get('start_date', '2020-09-01')
            end_date = request.query_params.get('end_date', str(datetime.now().date()))
        if month_or_week is not None:
            if month_or_week == 'month':
                weeks_dates_in_period = self.get_month_dates_in_period(
                    start_date, end_date
                )
            else:
                weeks_dates_in_period = self.get_weeks_dates_in_period(
                    start_date, end_date
                )
        else:
            weeks_dates_in_period = self.get_weeks_dates_in_period(
                start_date, end_date
            )
        all_total = 0
        if total_users is not None:
            print(weeks_dates_in_period)
            for week in weeks_dates_in_period:
                start_date_, week_start_date, week_end_date = self.getStartDate(week, month_or_week)
                try:
                    week_start_date = str(week_start_date.date())
                except Exception as e:
                    week_start_date = str(week_start_date)
                try:
                    week_end_date_ = week_end_date.date()
                    week_end_date = str(week_end_date.date())

                except Exception as e:
                    week_end_date_ = week_end_date
                    week_end_date = str(week_end_date)
                if month_or_week == 'month':
                    if week_end_date_ > datetime.now().date():
                        disp = end_date
                    else:
                        disp = week_end_date
                else:
                    disp = start_date_

                curr_total = users.filter(
                            created__date__gte=start_date_,
                            created__date__lte=week_end_date
                        ).count()
                all_total += curr_total
                response.append(
                    {
                        'start_date': disp,
                        'total': curr_total,
                    }
                )
            response[0]['all_total'] = all_total
        elif location is not None:
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-07-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            locations = Location.objects.filter(is_active=True)
            users = users.filter(
                            created__gte=start_date,
                            created__lte=end_date
                        )
            for location in locations:
                response.append(
                    {
                        'location': location.name,
                        'count': users.filter(
                            location__name__icontains=location,
                        ).count()
                    }
                )
        elif user_account_type is not None:
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            print("users_count0={}".format(users.count()))
            for week in weeks_dates_in_period:
                start_date_, week_start_date, week_end_date = self.getStartDate(week, month_or_week)
                try:
                    week_end_date_ = week['month_date'].date()
                    week['month_date'] = str(week['month_date'].date())
                except Exception as e:
                    week['month_date'] = str(week['end_date'].date())
                try:
                    week_end_date_ = week['start_date'].date()
                    week['start_date'] = week['start_date'].date()
                except Exception as e:
                    pass

                if month_or_week == 'month':
                    if week_end_date_ > datetime.now().date():
                        disp = end_date
                    else:
                        disp = week_end_date.date()
                else:
                    disp = str(start_date_)

                curr_users = users.filter(
                        created__date__gte=week['start_date'],
                        created__date__lte=week['month_date']
                    )

                response.append(
                    {   'week': disp,
                        'data':{
                            'individual': curr_users.filter(account_type=Choice.INDIVIDUAL).count(),
                            'group': curr_users.filter(account_type=Choice.GROUP).count()
                        }
                    }
                )
        return response