from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status

import pytz
import calendar
from datetime import datetime, timedelta, date

from data_tracking.models import QuestionTracking, LesssonTracking
from utils.choices import Choice
from users.models import User
from learning.models import Location, Lesson, Question, Category


class BaseUptakeLessonCompletionStats:
    def __init__(self, request, lessons, users):
        self.request = request
        self.lessons = lessons
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

    def time_to_eat(self, start_time, timezone="Africa/Nairobi"):
        # local = pytz.timezone(timezone)
        # local_dt = local.localize(naive, is_dst=None)
        # eat_dt = local_dt.astimezone(pytz.eat)
        # return eat_dt
        # utcmoment = naive.replace(tzinfo=pytz.utc)
        # localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
        # return localDatetime.strftime("%Y-%m-%d %H:%M:%S")

        timezone = "Africa/Nairobi"
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z')
        utcmoment = start_time.replace(tzinfo=pytz.utc)
        localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
        start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')



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


        if filter == 'users_total_per_lesson':
            for lesson in self.lessons:
                response.append(
                    {
                        'lesson': '{}: {}'.format(lesson.order, lesson.description),
                        'total': self.getUsersCompletedLesson(lesson, start_date, end_date)[0],
                    }
                )
        elif filter == 'location_of_completing_lesson':
            #Provide the filter=location_of_completing_modules and the location id

            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-07-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            locations = Location.objects.filter(is_active=True)

            for location in locations:
                users_completed = self.getUsersCompletedLesson(self.lessons.last(), start_date, end_date)[1]
                count = 0
                for user_completed in users_completed:
                    if user_completed.location == location:
                        count += 1
                response.append(
                    {
                        'location': location.name,
                        'total': count,
                    }
                )
        elif filter == 'time_taken_to_complete_lessons':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            print("start_date={}".format(start_date))
            print("end_date={}".format(end_date))


            for lesson in self.lessons:
                users_completed = self.getUsersCompletedLesson(lesson, start_date, end_date)[1]
                print("lesson={}".format(lesson.order))
                print("users_completed={}".format(len(users_completed)))

                total_time_to_complete_module = 0
                for user in users_completed:
                    try:
                        start_time = LesssonTracking.objects.filter(
                            lesson=lesson,
                            user=user
                        ).order_by('created').first()
                        start_time = start_time.data[0]['end_time']

                        end_time = LesssonTracking.objects.filter(
                            lesson=lesson,
                            user=user
                        ).order_by('created').last().data[0]['end_time']

                        start_time = self.time_to_eat(start_time)
                        end_time = self.time_to_eat(end_time)

                        diff_minutes = (end_time - start_time).total_seconds() / 60
                        if diff_minutes < 0:
                            diff_minutes = diff_minutes*-1
                        total_time_to_complete_module += diff_minutes
                    except Exception as e:
                        total_time_to_complete_module = 0
                        print("Error:{}".format(e))

                total_users = len(users_completed) if len(users_completed) > 0 else 1
                average_time = total_time_to_complete_module/total_users

                response.append(
                    {   'lesson': '{}: {}'.format(lesson.order, lesson.description),
                        'time_taken': round(average_time, 2)
                    }
                )

        elif filter == 'user_type_completing_lesson':
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

                lesson = self.lessons.last()
                users_completing = self.getUsersCompletedLesson(lesson, start_date_, week_start_date)[1]
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
        elif filter == 'users_total_completing_lesson':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

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


                lesson = self.lessons.last()
                users_completing = self.getUsersCompletedLesson(lesson, start_date_, week_start_date)[0]

                response.append(
                    {   'week': disp,
                        'total': users_completing
                    }
                )

        elif filter == '':

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
                print("week_start_date={}".format(week_start_date))
                print("week_end_date={}".format(week_end_date))
                response.append(
                    {
                        # 'lesson': '{}: {}'.format(self.lesson.order, self.lesson.description),
                        'total': self.getUsersCompletedLesson(self.lesson, week_start_date, week_end_date)[0],
                        'start_date': week_start_date,
                        'end_date': week_end_date
                    }
                )


        elif filter == 'users_number_per_module':
            for module in modules:
                response.append(
                    {
                        'lesson': '{}: {}'.format(module.order, module.name),
                        # 'total': self.getUsersCompletedModule(module)[0],
                        'total': self.getUsersCompletedLesson(
                            self, self.lesson, start_date=None, end_date=None
                        )[0]
                    }
                )

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
                print("week_start_date={}".format(week_start_date))
                print("week_end_date={}".format(week_end_date))
                response.append(
                    {
                        # 'lesson': '{}: {}'.format(self.lesson.order, self.lesson.description),
                        'total': self.getUsersCompletedLesson(self.lesson, week_start_date, week_end_date)[0],
                        'start_date': week_start_date,
                        'end_date': week_end_date
                    }
                )


        elif filter == 'time_taken_to_complete_module':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            modules = Category.objects.all()
            for module in modules:
                users_completed = self.getUsersCompletedModule(module)[1]

                print("users_completed={}: {}".format(module.order, users_completed))

                module_lessons = Lesson.objects.filter(
                    category=module
                )
                module_first_lesson = module_lessons.filter(
                    order=1
                ).last()
                module_last_lesson = module_lessons.filter(
                    order=module_lessons.count()
                ).last()

                total_time_to_complete_module = 0

                for user in users_completed:
                    try:
                        print("Got here 1")
                        start_time = LesssonTracking.objects.filter(
                            lesson=module_first_lesson,
                            user=user
                        ).order_by('created').first()
                        start_time = start_time.data[0]['end_time']
                        print("Got here 3")

                        end_time = LesssonTracking.objects.filter(
                            lesson=module_last_lesson,
                            user=user
                        ).order_by('created').first().data[0]['end_time']

                        # start_time = start_time.split(" +0")[0]
                        # end_time = end_time.split(" +0")[0]
                        # start_time = self.time_to_eat(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z'))
                        # end_time = self.time_to_eat(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f %z'))

                        start_time = self.time_to_eat(start_time)
                        end_time = self.time_to_eat(end_time)

                        diff_minutes = (end_time - start_time).total_seconds() / 60
                        print("diff_minutes={}".format(diff_minutes))
                        if diff_minutes < 0:
                            diff_minutes = diff_minutes*-1
                        total_time_to_complete_module += diff_minutes
                    except Exception as e:
                        total_time_to_complete_module = 0
                        print("Error:{}".format(e))

                total_users = len(users_completed) if len(users_completed) > 0 else 1
                average_time = total_time_to_complete_module/total_users

                response.append(
                    {   'module': '{}: {}'.format(module.order, module.name),
                        'time_taken': round(average_time, 2)
                    }
                )


        elif filter == 'users_number_per_module_period':
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
                print("week_start_date={}".format(week_start_date))
                print("week_end_date={}".format(week_end_date))

                for module in modules:
                    response.append(
                        {
                            'module': module.name,
                            'total': self.getUsersCompletedModule(module, week_start_date, week_end_date)[0],
                            'start_date': week_start_date,
                            'end_date': week_end_date
                        }
                    )

        return response