from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status

import csv
import pytz
import calendar
from datetime import datetime, timedelta, date

# from dashboard.utils.progress.excel_utils import create_excel_file
from dashboard.utils.progress.email_utils import send_email
from dashboard.utils.progress_through_modules_cache import createUserCompletedModulesStats
from data_tracking.models import QuestionTracking, LesssonTracking, CategoryTracking, LessonCompletionStats, \
    UserCompletedModulesStats, CategoryTrackingStats
from lenga.settings.local import TEST_USERS_LIST, EXCLUDE_START_DATE
from utils.choices import Choice
from users.models import User
from learning.models import Location, Lesson, Question, Category


class BaseProgressStats:
    def __init__(self, request, modules, users):
        self.request = request
        self.modules = modules
        self.users = users


    def getUserModuleCompletedLessons(self, user, module, start_date, end_date, user_lessons_completed=[]):
        lessons_count = 0
        lessons_list = []

        ####
        user_lessons_completed = LessonCompletionStats.objects.filter(
            start_date__gte=start_date,
            end_date__lte=end_date,
            lesson__category=module
        )



        ##

        # user = self.users.last()
        print("start_date={}".format(start_date))
        print("end_date={}".format(end_date))
        lessons = Lesson.objects.filter(category=module)
        for lesson in lessons:
            lesson_questions = Question.objects.filter(
                lesson=lesson, is_active=True
            )

            quests_responses = QuestionTracking.objects.filter(
                question__in=lesson_questions,
                user=user
            )

            user_completed_questions = []
            for lesson_question in lesson_questions:
                user_quests_responses = quests_responses.filter(
                    question=lesson_question
                )
                if user_quests_responses:
                    lesson_tracking = LesssonTracking.objects.filter(
                        lesson=lesson,
                        user=user
                    ).order_by('created')
                    if lesson_tracking:
                        # lesson_tracking = lesson_tracking.last()
                        lessons_end_dates = []
                        for lesson_ in lesson_tracking:
                            lessons_end_dates.append(lesson_.data[0]['end_time'])
                        endTime = max(lessons_end_dates)
                        # endTime = lesson_tracking.data[0]['end_time']
                        endTime = self.time_to_eat(endTime).date()
                        start_date = datetime.strptime(str(start_date), "%Y-%m-%d").date()
                        try:
                            end_date = datetime.strptime(str(end_date), "%Y-%m-%d").date()
                        except Exception as e:
                            end_date = datetime.strptime(str(end_date), "%Y-%m-%d %H:%M:%S").date()
                        print("Lesson last date={}".format(endTime))

                        if start_date <= endTime  and end_date >= endTime:
                            user_completed_questions.append(lesson_question)

            user_completed_questions = list(set(user_completed_questions))
            if len(user_completed_questions) == lesson_questions.count():
                lessons_count += 1
                lessons_list.append(lesson)

        return lessons_count, lessons_list


    def getDetailedUserModuleCompletedLessons(self, user, module, start_date, end_date):
        lessons_count = 0
        lessons_list = []

        lessons = Lesson.objects.filter(category=module)
        for lesson in lessons:
            lesson_questions = Question.objects.filter(
                lesson=lesson,is_active=True
            )

            quests_responses = QuestionTracking.objects.filter(
                question__in=lesson_questions,
                user=user
            )
            duration = 0.0
            no_of_times_taken = 0
            endTime_ = ''

            user_completed_questions = []
            for lesson_question in lesson_questions:
                user_quests_responses = quests_responses.filter(
                    question=lesson_question
                )
                if user_quests_responses:
                    lesson_tracking = LesssonTracking.objects.filter(
                        lesson=lesson,
                        user=user
                    ).order_by('created')
                    no_of_times_taken = lesson_tracking.count()
                    if lesson_tracking:
                        # lesson_tracking = lesson_tracking.last()
                        lessons_end_dates = []
                        for lesson_ in lesson_tracking:
                            lessons_end_dates.append(lesson_.data[0]['end_time'])
                        endTime = max(lessons_end_dates)
                        startTime = min(lessons_end_dates)

                        startTime_ = self.time_to_eat(startTime)
                        endTime_ = self.time_to_eat(endTime)
                        endTime = self.time_to_eat(endTime).date()
                        start_date = datetime.strptime(str(start_date), "%Y-%m-%d").date()
                        try:
                            end_date = datetime.strptime(str(end_date), "%Y-%m-%d").date()
                        except Exception as e:
                            end_date = datetime.strptime(str(end_date), "%Y-%m-%d %H:%M:%S").date()



                        if endTime >= start_date  and endTime <= end_date:
                            user_completed_questions.append(lesson_question)
                            if endTime_ == '':
                                endTime_ = lesson_tracking.last().created
                            if startTime_ == '':
                                startTime_ = lesson_tracking.first().created

                            duration = (self.time_to_eat(endTime_) - self.time_to_eat(startTime_)).total_seconds() / 60
                elif lesson_question.question_type.upper() == 'VIDEO':
                    user_quests_response = user_quests_responses.last()
                    if user_quests_response is None:
                        duration = 0
                    else:
                        startTime_ = self.time_to_eat(user_quests_response[0]['startTime'])
                        endTime = self.time_to_eat(user_quests_response[0]['endTime'])
                        duration = (self.time_to_eat(endTime_) - self.time_to_eat(startTime_)).total_seconds() / 60





            user_completed_questions = list(set(user_completed_questions))
            if len(user_completed_questions) == lesson_questions.count():
                lessons_count += 1
                lessons_list.append(
                    {
                        'lesson': lesson,
                        'duration': duration,
                        'time_of_completion': '{}'.format(str(endTime_)),
                        'no_of_times_taken': no_of_times_taken
                     }
                )

        return lessons_count, lessons_list

    def getUserCompletedModules(self, user, start_date=None, end_date=None, user_lessons_completed=[]):
        user_completed_modules = []
        modules = self.modules
        for module in modules:
            user_module_lessons_completed = user_lessons_completed.filter(
                lesson__category=module
            )
            module_lessons = Lesson.objects.filter(
                category=module
            )

            completed_lessons_count = user_module_lessons_completed.count()
            if completed_lessons_count == module_lessons.count():
                user_completed_modules.append(module)
                first_lesson_completed = user_module_lessons_completed.filter(
                    order=1
                )
                last_lesson_completed = user_module_lessons_completed.filter(
                    order=module_lessons.count()
                )
                UserCompletedModulesStats.objects.get_or_create(
                    user=user,
                    module=module,
                    start_date=first_lesson_completed.start_date,
                    completion_date=last_lesson_completed.end_date
                )

        return len(user_completed_modules), user_completed_modules,

    def getAverageModulesCompleted(self, start_date=None, end_date=None):
        users = self.users

        #Average modules completed = (modules completed * number of users who completed modules)/total no. of users






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
        start_time = str(start_time)
        try:
            timezone = "Africa/Nairobi"
            start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S.%f %z')
            utcmoment = start_time.replace(tzinfo=pytz.utc)
            localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
            start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            pass
        try:
            return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return datetime.strptime('{} 00:00:00'.format(start_time), '%Y-%m-%d %H:%M:%S')



    def getData(self):
        request = self.request
        users = self.users.exclude(
                username__icontains='test'
            ).exclude(username__in=TEST_USERS_LIST).exclude(
            created__date__lt=EXCLUDE_START_DATE
            )
        self.users = users

        start_date = request.query_params.get('start_date', None)
        if start_date == '2020-09-01':
            start_date = EXCLUDE_START_DATE
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

        if filter == 'average_modules_completed':
            user_completed_modules = UserCompletedModulesStats.objects.filter()
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
                print("week_start_date={}".format(start_date_))
                print("week_end_date={}".format(week_end_date))

                completed_total = 0


                ######
                user_completed_modules1 = user_completed_modules.filter(
                    completion_date__date__gte=start_date_,
                    completion_date__date__lte=week_end_date
                )

                unique_users = list(set([u.user for u in user_completed_modules1]))


                ######
                for user in unique_users:#self.users:
                    completed_total += user_completed_modules1.filter(user=user).count()

                # completed_count_average = completed_total/self.users.count()
                completed_count_average = completed_total / (self.modules.count() * self.users.count())
                completed_count_average = completed_count_average * 100

                response.append(
                    {
                        'modules_completed': round(completed_count_average, 2),
                        'start_date': week_start_date,
                        'end_date': week_end_date
                    }
                )
        elif filter == 'average_modules_completed_by_user_type':
            print("GOT HERE USER TYPE")
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except Exception as e:
                pass
            user_completed_modules = UserCompletedModulesStats.objects.filter(
                completion_date__date__gte=start_date,
                completion_date__date__lte=end_date
            )

            users = self.users
            individuals_count = 0
            group_count = 0

            for u in users:
                if u.account_type == Choice.INDIVIDUAL:
                    individuals_count += 1
                else:
                    group_count += 1


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

                individuals_completed_total = 0
                # individuals_count = 0
                group_completed_total = 0
                # group_count = 0

                ####
                unique_users = []
                for u in user_completed_modules:
                    print("COMPLETION DATE={}:{}".format(u.completion_date.date(), u.user.id))
                    if u.user not in unique_users:
                        unique_users.append(u.user)
                print("self.users={}".format(self.users.count()))
                try:
                    start_date_ = datetime.strptime(start_date_, '%Y-%m-%d').date()
                    week_end_date = datetime.strptime(week_end_date, '%Y-%m-%d').date()
                except Exception as e:
                    pass
                user_completed_modules1 = user_completed_modules.filter(
                    completion_date__gte=start_date_,
                    completion_date__lte=week_end_date
                )
                print("3::::start_date={}".format(start_date_))
                print("3::::end_date={}".format(week_end_date))

                print("2:::user_completed_modules={}".format(user_completed_modules1.count()))
                for user in unique_users:#self.users:
                    user_completed_modules1 = user_completed_modules1.filter(
                        user=user,
                    )
                    completed_count = user_completed_modules1.count()

                    if user.account_type == Choice.INDIVIDUAL:
                        individuals_completed_total += completed_count
                    else:
                        group_completed_total += completed_count

                individuals_count = individuals_count if individuals_count > 0 else 1
                group_count = group_count if group_count > 0 else 1

                individuals_average = individuals_completed_total/individuals_count
                group_average = group_completed_total / group_count

                # (self.modules.count() * self.users.count())

                individuals_average = round(individuals_average * 100, 2)
                group_average = round(group_average * 100, 2)

                response.append(
                    {
                        'individuals_modules_completed': individuals_average,
                        'group_modules_completed': group_average,
                        'start_date': start_date_,
                        'end_date': week_end_date
                    }
                )
        elif filter == 'average_modules_completed_by_location':
            # users_lessons_completed = LessonCompletionStats.objects.filter(
            #     start_date__gte=start_date,
            #     end_date__lte=end_date,
            # )

            user_completed_modules = UserCompletedModulesStats.objects.filter(
                completion_date__date__gte=start_date,
                completion_date__date__lte=end_date
            )

            unique_users = list(set([u.user for u in user_completed_modules]))

            locations = Location.objects.filter(is_active=True)
            for location in locations:
                location_completed_total = 0
                location_users_count = len(list(
                    set(
                        [u for u in self.users if u.location == location]
                    )))
                for user in unique_users:#self.users:
                    # user_lessons_completed = users_lessons_completed.filter(
                    #     user=user
                    # )
                    # completed_count, completed_modules = self.getUserCompletedModules(
                    #     user, start_date, end_date, user_lessons_completed
                    # )
                    if user.location == location:
                        location_completed_total += user_completed_modules.filter(
                            user=user
                        ).count()
                        # location_users_count += 1

                location_users_count = location_users_count if location_users_count > 0 else 1
                location_average = location_completed_total / location_users_count

                response.append(
                    {
                        'location': location.name,
                        'modules_completed': round((location_average * 100), 2),
                        'start_date': start_date,
                        'end_date': end_date
                    }
                )

        elif filter == 'lessons_completed_in_a_module':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))
            lessons_completed = LessonCompletionStats.objects.filter(
                end_date__date__gte=start_date,
                end_date__date__lte=end_date,
            )
            for module in self.modules:
                lessons_completed1 = lessons_completed.filter(
                    lesson__category=module
                ).count()

                users_count = self.users.count() if self.users.count() > 0 else 1
                completed_lessons_average = lessons_completed1/users_count #total_completed_lessons/users_count

                response.append({
                        'module': '{}: {}'.format(module.order, module.name),
                        'lessons_completed': round(completed_lessons_average * 100, 2) #lessons_completed1#completed_lessons_average,
                    })

        elif filter == 'lessons_completed_in_a_module_user_type':
            print("HERE")
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))


            lessons_completed = LessonCompletionStats.objects.filter(
                end_date__date__gte=start_date,
                end_date__date__lte=end_date,
            )


            individuals_users_count = 0
            group_users_count = 0

            for u in self.users:
                if u.account_type == Choice.INDIVIDUAL:
                    individuals_users_count += 1
                else:
                    group_users_count += 1

            for module in self.modules:
                individuals_total_completed_lessons = 0
                group_total_completed_lessons = 0

                lessons_completed1 = lessons_completed.filter(
                    lesson__category=module
                )
                for lessons_completed_ in lessons_completed1:
                    if lessons_completed_.user.account_type == Choice.INDIVIDUAL:
                        individuals_total_completed_lessons += 1
                        # individuals_users_count += 1
                    else:
                        group_total_completed_lessons += 1
                        # group_users_count += 1
                ##
                individuals_users_count = individuals_users_count if individuals_users_count > 0 else 1
                group_users_count = group_users_count if group_users_count > 0 else 1
                individuals_completed_lessons_average = individuals_total_completed_lessons/individuals_users_count
                groups_completed_lessons_average = group_total_completed_lessons / group_users_count

                response.append({
                        'module': '{}: {}'.format(module.order, module.name),
                        'individuals_lessons_completed': round(individuals_completed_lessons_average * 100, 2),
                        'groups_lessons_completed': round(groups_completed_lessons_average * 100, 2),
                    })

        elif filter == 'lessons_completed_in_a_module_location':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            lessons_completed = LessonCompletionStats.objects.filter(
                end_date__date__gte=start_date,
                end_date__date__lte=end_date,
            )

            lessons_count = Lesson.objects.all().count()
            locations = Location.objects.filter(is_active=True)
            for location in locations:
                # location_total_completed_lessons = 0
                location_users_count = self.users.filter(
                    location=location
                ).count()

                location_total_completed_lessons = lessons_completed.filter(
                    user__location=location
                ).count()
                ###

                location_users_count = location_users_count if location_users_count > 0 else 1
                location_completed_lessons_average = location_total_completed_lessons/(location_users_count * lessons_count)

                response.append({
                        'location': location.name,
                        'location_lessons_completed': round(location_completed_lessons_average * 100, 2),
                    })


        elif filter == 'modules_repeated':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))



            data = []
            # module_takes = CategoryTracking.objects.filter()
            module_takes = CategoryTrackingStats.objects.filter()
            users = list(set([u.user.id for u in module_takes]))
            modules = Category.objects.all()
            for module in modules: #self.modules:
                # module_takes = CategoryTracking.objects.filter(
                #     user=self.users.last(), category=module
                # )
                module_takes_count = 0
                for u in users:
                    module_takes1 = module_takes.filter(
                        user=u, module=module
                    )
                    for mod_take in module_takes1:
                        start_date = datetime.strptime(str(start_date), "%Y-%m-%d").date()
                        end_date = datetime.strptime(str(end_date), "%Y-%m-%d").date()
                        # date_time = self.time_to_eat(mod_take.data[0]['start_time']).date()
                        date_time = self.time_to_eat(mod_take.start_date.date()).date()
                        print("date_time={}".format(date_time))
                        print("date_time type={}".format(type(date_time)))

                        print("start_date={}".format(start_date))
                        print("start_date type={}".format(type(start_date)))

                        print("end_date={}".format(end_date))
                        print("end_date type={}".format(type(end_date)))
                        if start_date <= date_time and end_date >= date_time:
                            module_takes_count += 1
                response.append({
                    'module': '{} {}'.format(module.order, module.name),
                    'repeated_count': module_takes_count,
                })



        elif filter == 'all_users_stats':
            email = request.query_params.get('email', None)
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-07-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            print("START DATE = {}".format(start_date))
            print("END DATE = {}".format(end_date))


            labels = ["username", "user_type", "location","created"]
            for module in self.modules:
                for lesson in Lesson.objects.filter(category=module):
                    labels.append("module_{}_lesson_{}".format(module.order, lesson.order))
                    labels.append("module_{}_lesson_{}_duration".format(module.order, lesson.order))
                    labels.append("module_{}_lesson_{}_time_of_completion".format(module.order, lesson.order))
                    labels.append("module_{}_lesson_{}_number_of_times_taken".format(module.order, lesson.order))

            records = []
            for user in self.users:
                user_details = {}

                created_at = user.created
                time_ = '{}:{}:{}'.format(created_at.hour, created_at.minute, created_at.second)

                try:
                    user_location = user.location.name
                except Exception as e:
                    user_location = ''



                username = user.username
                # username = '{}_{}'.format(user.username, user.first_name)

                ##Determine the username
                if 'androidx.appcompat.widget'.upper() in username.upper():
                    username = user.first_name
                elif username.count("_") >= 2:
                    username = user.first_name
                ##End of determine the username
                user_details['username'] = username  # user.username
                user_details['user_type'] = user.account_type
                user_details['location'] = user_location
                user_details['created'] = '{} {}'.format(str(created_at.date()), time_)

                # data = [
                #     user.first_name, user.account_type,
                #     user_location, '{} {}'.format(str(created_at.date()), time_)
                # ]
                data = [
                    username, user.account_type,
                    user_location, '{} {}'.format(str(created_at.date()), time_)
                ]
                for module in self.modules:
                    count, lessons_completed = self.getDetailedUserModuleCompletedLessons(
                        user, module, start_date, end_date
                    )
                    lessons_list = [lesson1['lesson'] for lesson1 in lessons_completed]
                    # data.append(module.name)
                    lessons_all = Lesson.objects.filter(category=module)
                    for lesson_main in lessons_all:
                        less = None
                        for lesson in lessons_completed:
                            print(lesson)
                            lesson_ = lesson['lesson']
                            if lesson_main in lessons_list and lesson_ == lesson_main: #== lesson1:
                                lesson_name = '{}: {}'.format(lesson_.description, lesson_.order)
                                lesson_name = 'Completed'

                                duration = lesson['duration']
                                try:
                                    duration = float(duration)
                                except Exception as e:
                                    duration = 0.0
                                time_of_completion = lesson['time_of_completion']
                                try:
                                    time_of_completion = float(time_of_completion)
                                    time_of_completion = ''
                                except Exception as e:
                                    time_of_completion = time_of_completion
                                no_of_times_taken = lesson['no_of_times_taken']
                                try:
                                    no_of_times_taken = int(no_of_times_taken)
                                except Exception as e:
                                    no_of_times_taken = no_of_times_taken
                                less = True
                                break
                            if less is not None:
                                break
                        if less is not None:
                            data.append(lesson_name)
                            data.append(duration)
                            data.append(time_of_completion)
                            data.append(no_of_times_taken)
                        else:
                            data.append('Not completed')
                            data.append(0)
                            data.append('')
                            data.append(0)
                records.append(data)

            file_link = "/projects/lenga/media/tmp/data_{}.csv".format(datetime.now())
            with open(file_link, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(labels)
                for data in records:
                    writer.writerow(data)
            send_email(start_date, end_date, file_link, email)
            response.append({'message': 'Export will be sent to your email'})








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