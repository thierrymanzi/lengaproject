from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status

import pytz
import calendar
from datetime import datetime, timedelta, date

from dashboard.utils.modules_completion import BaseUptakeModuleCompletionStats
from dashboard.utils.progress_through_modules_cache import loadModulesProgressStats
from data_tracking.models import (
    QuestionTracking,
    LesssonTracking,
    CategoryTracking,
    ModuleQuestionsCompletedStats,
    CategoryTrackingStats
)
from utils.choices import Choice
from users.models import User
from learning.models import Location, Lesson, Question, Category


class BaseUsageStats:
    def __init__(self, request, modules, users):
        self.request = request
        self.modules = modules
        self.users = users


    def getUsersCompletedLesson(self, lesson, start_date=None, end_date=None):
        users_count = 0
        users_list = []
        lesson_questions = Question.objects.filter(
            lesson=lesson, is_active=True
        )

        quests_responses = QuestionTracking.objects.filter(
            question__id__in=[q.id for q in lesson_questions]
        )

        for user in self.users:
            user_completed_questions = []
            # user_quests_responses = quests_responses.filter(
            #     user=user
            # )
            for lesson_question in lesson_questions:
                user_quests_responses = quests_responses.filter(
                    question=lesson_question, user=user
                )
                if user_quests_responses:
                    if start_date is not None and end_date is not None:
                        lesson_tracking = LesssonTracking.objects.filter(
                            lesson=lesson,
                            user=user
                        ).order_by('created')
                        if lesson_tracking:
                            lesson_tracking = lesson_tracking.last()
                            endTime = lesson_tracking.data[0]['end_time']
                            endTime = self.time_to_eat(endTime).date()
                            start_date = datetime.strptime(str(start_date), "%Y-%m-%d").date()
                            try:
                                end_date = datetime.strptime(str(end_date), "%Y-%m-%d").date()
                            except Exception as e:
                                end_date = datetime.strptime(str(end_date), "%Y-%m-%d %H:%M:%S").date()

                            if endTime >= start_date and endTime <= end_date:
                                user_completed_questions.append(lesson_question)
                    else:
                        user_completed_questions.append(lesson_question)

            user_completed_questions = list(set(user_completed_questions))
            if len(user_completed_questions) == lesson_questions.count():
                users_count += 1
                users_list.append(user)

        return users_count, users_list

    def getUsersCompletedModule(self, module, start_date=None, end_date=None):
        users_completed_module_count = 0
        users_completed_module = []
        module_lessons = Lesson.objects.filter(
            category=module
        )

        users_in_lessons = []
        for module_lesson in module_lessons:
            completed_count, users_completed = self.getUsersCompletedLesson(
                module_lesson, start_date, end_date
            )

            users_in_lessons.append(
                {
                    'lesson': module_lesson,
                    'users': users_completed
                }
            )


        for user in self.users:
            lesson_completion_appearance_count = 0
            for user_in_lesson in users_in_lessons:
                if user in user_in_lesson['users'] and module == user_in_lesson['lesson'].category:
                    lesson_completion_appearance_count += 1
            if lesson_completion_appearance_count == module_lessons.count():
                users_completed_module_count += 1
                users_completed_module.append(user)

        return users_completed_module_count, users_completed_module














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
                        'end_date': (curr_date + timedelta(days=6)).date()
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

    def time_to_eat(self, start_time, timezone="Africa/Nairobi"):
        # local = pytz.timezone(timezone)
        # local_dt = local.localize(naive, is_dst=None)
        # eat_dt = local_dt.astimezone(pytz.eat)
        # return eat_dt
        # utcmoment = naive.replace(tzinfo=pytz.utc)
        # localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
        # return localDatetime.strftime("%Y-%m-%d %H:%M:%S")

        timezone = "Africa/Nairobi"
        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z')
        except Exception as e:
            try:
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S%z')
            except Exception as e:
                start_time = datetime.strptime(str(start_time).split("+")[0], '%Y-%m-%d %H:%M:%S')
        utcmoment = start_time.replace(tzinfo=pytz.utc)
        localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
        start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')


    def getDurationSessions(self, start_date, end_date):

        period_sesssions = []
        week_sessions_users = []
        total_week_sess_duration = 0.0

        for session in self.sessions:
            try:
                session_start = session.start_date
                session_end = session.completion_date
                # session_start = self.time_to_eat(session_start)
                # session_end = self.time_to_eat(session_end)
                session_start = self.time_to_eat(str(session_start))
                session_end = self.time_to_eat(str(session_end))
                week_start_date_ = datetime.strptime(str(start_date), "%Y-%m-%d").date()
                week_end_date_ = datetime.strptime(str(end_date), "%Y-%m-%d").date()
                if session_start.date() >= week_start_date_ and session_end.date() <= week_end_date_:
                    sess_duration = ((session_end - session_start).total_seconds()) / 60
                    total_week_sess_duration += sess_duration
                    week_sessions_users.append(session.user)
                    period_sesssions.append(
                        {
                            'session': session,
                            'duration': sess_duration,
                            'user_type': session.user.account_type
                        }
                    )
            except Exception as e:
                print("Error:{}-{}: {}".format(start_date, end_date, e))

        return total_week_sess_duration, list(set(week_sessions_users)), period_sesssions



    def getData(self):
        """
        Session duration:
        sessions = Module
        :return:
        """

        # self.sessions = CategoryTracking.objects.filter(user__in=self.users) #If user not define, give for all users
        self.sessions = CategoryTrackingStats.objects.filter(user__in=self.users)
        # sessions_users  = list(set([s.user for s in sessions]))

        # for session in sessions:
        #     session_start = session['start_date']
        #     session_end = session['end_date']

            # Total=Period: give start & end date: give sess_durations for the periods:
            # sess_duration = ((session_end - session_start).total_sesconds()) / 60

            #User: give user, start & end date: give sess_durations for the periods:
            #Location: give location, start & end date: give sess_durations for the periods for the location:


        request = self.request
        users = self.users

        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        user_account_type = request.query_params.get('user_account_type', None)
        location = request.query_params.get('location', None)
        module_id = request.query_params.get('module', None)
        filter = request.query_params.get('filter', None)





        if module_id is not None:
            modules = Category.objects.filter(id=module_id)
        else:
            modules = Category.objects.all()

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

        if filter == 'session_duration_total':

            for week in weeks_dates_in_period:
                start_date_, week_start_date, week_end_date = self.getStartDate(week, month_or_week)
                try:
                    week_start_date = str(week_start_date.date())
                except Exception as e:
                    week_start_date = str(week_start_date)
                try:
                    week_end_date = str(week_end_date.date())
                except Exception as e:
                    week_end_date = str(week_end_date)

                total_week_sess_duration, week_sessions_users,\
                period_sesssions = self.getDurationSessions(
                    start_date_, week_end_date
                )

                total_users = len(week_sessions_users) if len(week_sessions_users) > 0 else 1
                average_duration = (total_week_sess_duration) / total_users
                response.append(
                    {
                        'total_duration': round(average_duration, 2),
                        'start_date': start_date_,
                        'end_date': week_end_date
                    }
                )

        elif filter == 'session_duration_total_user_type':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            for week in weeks_dates_in_period:
                start_date_, week_start_date, week_end_date = self.getStartDate(week, month_or_week)

                try:
                    week_end_date = week_end_date.date()
                except Exception as e:
                    pass
                if month_or_week == 'month':
                    if week_end_date > datetime.now().date():
                        disp = end_date
                    else:
                        disp = week_end_date
                else:
                    disp = str(start_date_)


                total_week_sess_duration, sessions_users, \
                period_sesssions = self.getDurationSessions(
                    start_date_, week_end_date
                )

                individuals_count  = 0
                group_count = 0

                for u in sessions_users:
                    if u.account_type == Choice.INDIVIDUAL:
                        individuals_count += 1
                    else:
                        group_count += 1

                individuals_session_total = 0.0
                group_session_total = 0.0
                for session in period_sesssions:
                    if session['session'].user.account_type ==  Choice.INDIVIDUAL:
                        individuals_session_total += session['duration']
                    else:
                        group_session_total += session['duration']

                individuals_count = individuals_count if individuals_count > 0 else 1
                group_count = group_count if group_count > 0 else 1

                individuals_average_sess_duration = individuals_session_total / individuals_count
                group_average_sess_duration = group_session_total / group_count

                response.append(
                    {   'week': disp,
                        'data':{
                            'individual': round(individuals_average_sess_duration, 2),
                            'group': round(group_average_sess_duration, 2)
                        }
                    }
                )

        elif filter == 'session_duration_locations':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-07-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            locations = Location.objects.filter(is_active=True)
            total_week_sess_duration, sessions_users, \
            period_sesssions = self.getDurationSessions(
                start_date, end_date
            )


            for location in locations:

                location_users_count = 0
                location_session_total = 0.0
                for session in period_sesssions:
                    if session['session'].user.location == location:
                        location_session_total += session['duration']
                        location_users_count += 1

                location_users_count = location_users_count if location_users_count > 0 else 1
                location_average_sess_duration = location_session_total / location_users_count

                response.append(
                    {
                        'location': location.name,
                        'average_session_duration': round(location_average_sess_duration, 2)
                    }
                )
        elif filter == 'time_of_day_completed_modules':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            baseUptakeStats = BaseUptakeModuleCompletionStats(request, modules, self.users)
            for module in self.modules:

                users_completed_module_count, \
                users_completed_module = baseUptakeStats.getUsersCompletedModule(
                    module, start_date, end_date
                )
                if users_completed_module_count > 0:
                    module_lessons = LesssonTracking.objects.filter(
                        lesson__category=module
                    )
                    times = []
                    for module_lesson in module_lessons:
                        times.append(self.time_to_eat(module_lesson.data[0]['end_time']))
                    response.append(
                        {'module': '{}: {}'.format(module.order, module.name),
                         'average_completion_hour': max(times).time().hour
                         }
                    )
        elif filter == 'progress_through_modules':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            # baseUptakeStats = BaseUptakeModuleCompletionStats(request, modules, self.users)
            print("GOT HERE :::::::")
            competion_stats = ModuleQuestionsCompletedStats.objects.all()
            if not competion_stats:
                loadModulesProgressStats(self.modules, self.users)
            else:
                for module in self.modules:
                    competion_stats = ModuleQuestionsCompletedStats.objects.filter(
                        module=module,
                        completion_date__gte=start_date,
                        completion_date__lte=end_date,
                    )
                    total_items_in_module = competion_stats[0].total_items_in_module
                    completed_questions_in_module = competion_stats.count()

                    total_items_in_module = total_items_in_module * self.users.count()
                    total_items_in_module = total_items_in_module if total_items_in_module > 0 else 1

                    progress_percentage = round(
                        ((completed_questions_in_module/total_items_in_module) * 100), 2
                    )

                    response.append(
                        {'module': '{}: {}'.format(module.order, module.name),
                         'percentage_completion': progress_percentage
                         }
                    )
        elif filter == 'progress_through_modules_user_type':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            # baseUptakeStats = BaseUptakeModuleCompletionStats(request, modules, self.users)
            for module in self.modules:

                completion_stats = ModuleQuestionsCompletedStats.objects.filter(
                    module=module,
                    completion_date__gte=start_date,
                    completion_date__lte=end_date,
                )
                total_items_in_module = completion_stats[0].total_items_in_module
                ###
                individuals_completed_questions_in_module = 0
                group_completed_questions_in_module = 0

                for item in completion_stats:
                    if item.user.account_type == Choice.INDIVIDUAL:
                        individuals_completed_questions_in_module += 1
                    else:
                        group_completed_questions_in_module += 1

                individuals_total_items_in_module = total_items_in_module * len(
                    [u for u in self.users if u.account_type == Choice.INDIVIDUAL]
                )
                group_total_items_in_module = total_items_in_module * len(
                    [u for u in self.users if u.account_type == Choice.GROUP]
                )
                individuals_total_items_in_module = individuals_total_items_in_module if individuals_total_items_in_module > 0 else 1
                group_total_items_in_module = group_total_items_in_module if group_total_items_in_module > 0 else 1

                individuals_progress_percentage = round(
                    ((individuals_completed_questions_in_module / individuals_total_items_in_module) * 100), 2
                )

                group_progress_percentage = round(
                    ((group_completed_questions_in_module / group_total_items_in_module) * 100), 2
                )

                response.append(
                    {'module': '{}: {}'.format(module.order, module.name),
                     'data': {
                         'individual': individuals_progress_percentage,
                         'group': group_progress_percentage
                        }
                     }
                )

        elif filter == 'progress_through_modules_location':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            # baseUptakeStats = BaseUptakeModuleCompletionStats(request, modules, self.users)
            locations = Location.objects.filter(is_active=True)
            # for module in self.modules:
                # print("Module={}".format(module.id))

            completion_stats = ModuleQuestionsCompletedStats.objects.filter(
                completion_date__gte=start_date,
                completion_date__lte=end_date,
            )
            total_items_in_modules = 0
            modules_done = []
            for module in self.modules:
                module_completion_stats = completion_stats.filter(
                    module=module
                )
                for completion_stat in module_completion_stats:
                    if module not in modules_done:
                        total_items_in_modules += completion_stat.total_items_in_module
                modules_done.append(module)

            for location in locations:
                location_completed_questions_in_modules = completion_stats.filter(
                    user__location=location
                ).count()

                location_total_items_in_modules = total_items_in_modules * len(
                    [u for u in self.users if u.location == location]
                )

                location_total_items_in_modules = location_total_items_in_modules if location_total_items_in_modules > 0 else 1

                location_progress_percentage = round(
                    ((location_completed_questions_in_modules / location_total_items_in_modules) * 100), 2
                )

                response.append(
                    {'location': location.name,
                     'percentage_progress': location_progress_percentage
                     }
                )

        elif filter == 'user_type_completing_modules':
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


                print("start_date_={}".format(start_date_))
                print("week_end_date={}".format(week_start_date))

                users_completing = self.getUsersCompletedModule(modules.last(), start_date_, week_start_date)[1]
                individuals_count  = 0
                group_count = 0

                for u in users_completing:
                    if u.account_type == Choice.INDIVIDUAL:
                        individuals_count += 1
                    else:
                        group_count += 1

                response.append(
                    {   'week': disp,
                        'data':{
                            'individual': individuals_count,
                            'group': group_count
                        }
                    }
                )

        return response