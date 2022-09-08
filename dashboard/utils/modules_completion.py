from django.db.models import Count, F
from rest_framework.response import Response
from rest_framework import status

import json
import pytz
import calendar
from datetime import datetime, timedelta, date

from dashboard.utils.get_cache_from_file import getCacheFromFile, createFileCache
from data_tracking.models import QuestionTracking, LesssonTracking, LessonCompletionStats, LessonsStartedStats
from lenga.settings.local import CACHE_FILES_DIR
from utils.choices import Choice
from users.models import User
from learning.models import Location, Lesson, Question, Category


class BaseUptakeModuleCompletionStats:
    def __init__(self, request, modules, users):
        self.request = request
        self.modules = modules
        self.users = users


    def time_to_eat(self, start_time, timezone="Africa/Nairobi"):
        timezone = "Africa/Nairobi"
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z')
        utcmoment = start_time.replace(tzinfo=pytz.utc)
        localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
        start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    def getUsersCompletedLesson(self, lesson, start_date=None, end_date=None, module_questions=[], quests_tracking=[],create_stats_data=False):
        users_count = 0
        users_list = []

        lessons_completed = LessonCompletionStats.objects.filter(
            start_date__gte=start_date,
            end_date__lte=end_date,
            lesson=lesson
        )
        quests_tracking1 = None

        if create_stats_data is False:
            if lessons_completed:
                users_list = []
                for lessons_completed in lessons_completed:
                    users_list.append(lessons_completed.user)
                users_list = list(set(users_list))
                return len(users_list), users_list
            else:
                return 0, []
        else:
            if create_stats_data is True: #To create new
                # createFileCache(file_path, quests_tracking)
                print("HERE 2_1")
                # lesson_questions = Question.objects.filter(
                #     lesson=lesson, is_active=True
                # )

                lesson_questions = module_questions.filter(
                    lesson=lesson, is_active=True
                )


                quests_responses = quests_tracking.filter(
                    question__in=[q for q in lesson_questions]
                )

                lesson_trackings = LesssonTracking.objects.filter(
                    lesson=lesson,
                ).order_by('created')

                for user in self.users:
                    user_completed_questions = []
                    # user_quests_responses = quests_responses.filter(
                    #     user=user
                    # )
                    # lesson_trackings = LesssonTracking.objects.filter(
                    #     lesson=lesson,
                    # ).order_by('created')



                    min_start_times = []
                    max_end_times = []
                    lesson_tracking_checked_list =  []
                    is_video = False
                    video_start_date = None
                    video_end_date = None
                    video_duration = None

                    is_question = False
                    question_start_date = None
                    question_end_date = None
                    question_duration = None


                    user_lesson_trackings = lesson_trackings.filter(
                        user=user
                    )
                    start_date = datetime.strptime(str(start_date),
                                                   "%Y-%m-%d").date()
                    try:
                        end_date = datetime.strptime(str(end_date),
                                                     "%Y-%m-%d").date()
                    except Exception as e:
                        end_date = datetime.strptime(str(end_date),
                                                     "%Y-%m-%d %H:%M:%S").date()
                    for lesson_question in lesson_questions:
                        # if user_quests_responses:
                        user_quests_responses = quests_responses.filter(
                            question=lesson_question, user=user
                        )
                        if lesson_question.question_type == 'video':
                            # quest_video_tracking = user_quests_responses
                            found_item = False
                            found_item2 = False
                            # durations = []
                            # times = []
                            if user_quests_responses:
                                for video_data in user_quests_responses:
                                    for data_item in video_data.data:
                                        if data_item['question_id'] == str(lesson_question.id) and data_item[
                                            'type'] == 'ENDED':
                                            print(data_item)
                                            # startTime_ = self.time_to_eat(str(data_item['startTime']))
                                            # endTime_ = self.time_to_eat(str(data_item['endTime']))
                                            try:
                                                startTime_ = self.time_to_eat(str(data_item['startTime']))
                                            except Exception as e:
                                                startTime_ = self.time_to_eat(str(data_item['videoStartTime']))
                                            try:
                                                endTime_ = self.time_to_eat(str(data_item['endTime']))
                                            except Exception as e:
                                                endTime_ = self.time_to_eat(str(data_item['videoEndTime']))


                                            startTime = startTime_.date()
                                            endTime = endTime_.date()

                                            is_video = True
                                            video_start_date = startTime_
                                            video_end_date = endTime_
                                            # video_duration = data_item['duration']
                                            print("video_duration={}".format(video_duration))
                                            video_duration = (endTime_ - startTime_).total_seconds()
                                            # min_start_times.append(startTime_)
                                            # max_end_times.append(endTime_)
                                            found_item = True
                                            user_completed_questions.append(lesson_question)
                                            # durations.append(video_duration)
                                            # times.append({
                                            #     'video_start_date': video_start_date,
                                            #     'video_end_date': video_end_date
                                            # })
                                            # lesson_tracking_checked_list.append(video_tracking.id)
                                        if found_item is True:
                                            found_item2 = True
                                            break
                                    if found_item2 is True:
                                        break
                            elif user_lesson_trackings:
                                print("VIDEO HAS LESSON TRACKINGS:{}".format(lesson.order))
                                found_item3 = False
                                durations = []
                                times = []
                                for user_lesson_tracking in user_lesson_trackings:
                                    try:
                                        data = user_lesson_tracking.data
                                        found_item2 = False
                                        for data_item in data:
                                            if data_item['lesson_id'] == str(lesson.id):
                                                start_time = data_item['start_time']
                                                end_time = data_item['end_time']
                                                found_item = False
                                                if start_time not in ["", '', None] and end_time not in ["", '', None]:
                                                    startTime_ = self.time_to_eat(str(start_time))
                                                    endTime_ = self.time_to_eat(str(end_time))
                                                    startTime = startTime_.date()
                                                    endTime = endTime_.date()

                                                    is_video = True
                                                    video_start_date = startTime_
                                                    video_end_date = endTime_
                                                    # video_duration = data_item['duration']
                                                    print("video_duration={}".format(video_duration))
                                                    video_duration = (endTime_ - startTime_).total_seconds()
                                                    durations.append(video_duration)
                                                    times.append({
                                                        'video_start_date': video_start_date,
                                                        'video_end_date': video_end_date
                                                    })
                                                    # min_start_times.append(startTime_)
                                                    # max_end_times.append(endTime_)
                                                    # found_item = True
                                                    user_completed_questions.append(lesson_question)
                                                    #         if found_item is True:
                                                    #             found_item2 = True
                                                    #     if found_item2 is True:
                                                    #         found_item3 = True
                                                    #         break
                                                    # if found_item3 is True:
                                                    #     break
                                    except Exception as e:
                                        print(e)
                                try:
                                    max_time = max(durations)
                                    index_ = durations.index(max_time)
                                    is_video = True
                                    video_start_date = times[index_]['video_start_date']
                                    video_end_date = times[index_]['video_end_date']
                                    video_duration = max_time
                                except Exception as e:
                                    print("VIDEO ERROR:{}".format(e))

                        else:
                            found_item = False
                            if user_quests_responses:
                                start_date = datetime.strptime(str(start_date),
                                                               "%Y-%m-%d").date()
                                try:
                                    end_date = datetime.strptime(str(end_date),
                                                                 "%Y-%m-%d").date()
                                except Exception as e:
                                    end_date = datetime.strptime(str(end_date),
                                                                 "%Y-%m-%d %H:%M:%S").date()
                                #If there is user_quests_responses for this question, then the question was done, find the duration of the lesson
                                for lesson_tracking in user_lesson_trackings:
                                    datas = lesson_tracking.data
                                    found_item1 = False
                                    for data in datas:
                                        if data['lesson_id'] == str(lesson.id):
                                            startTime = data['start_time']
                                            startTime_ = self.time_to_eat(startTime)
                                            startTime = startTime_.date()

                                            endTime = data['end_time']
                                            endTime_ = self.time_to_eat(endTime)
                                            endTime = endTime_.date()
                                            # duration = (endTime_ - startTime_).total_seconds()
                                            min_start_times.append(startTime_)
                                            max_end_times.append(endTime_)

                                            user_completed_questions.append(lesson_question)
                                            lesson_tracking_checked_list.append(lesson_tracking.id)
                                            q_l = lesson_question.lesson
                                            if q_l.category.order == 2 and q_l.order == 3 and lesson_question.order == 1:
                                                lq = Question.objects.filter(
                                                    lesson__category__order=2,
                                                    lesson__order=3, order=2,
                                                    is_active=True
                                                ).last()
                                                user_completed_questions.append(lq)
                                                lesson_tracking_checked_list.append(lesson_tracking.id)
                                            if q_l.category.order == 5 and q_l.order == 5 and lesson_question.order == 1:
                                                lq = Question.objects.filter(
                                                    lesson__category__order=5,
                                                    lesson__order=5, order=2,
                                                    is_active=True
                                                ).last()
                                                user_completed_questions.append(lq)
                                                lesson_tracking_checked_list.append(lesson_tracking.id)
                                            found_item1 = True
                                        if found_item1 is True:
                                            found_item = True
                                            break
                                    if found_item is True:
                                        break

                    user_completed_questions = list(set(user_completed_questions))
                    if len(user_completed_questions) == lesson_questions.count():
                        print("Before creation")
                        users_count += 1
                        users_list.append(user)
                        user_completed_questions.append(lesson_question)

                        if is_video is True:
                            start_time_ = video_start_date
                            end_time_ = video_end_date
                            duration = video_duration
                        else:
                            # if is_question is True:
                            question_start_date = None
                            question_end_date = None
                            question_duration = None
                            start_time_ = min(min_start_times)
                            end_time_ = max(max_end_times)
                            duration = (end_time_ - start_time_).total_seconds()  # / 60

                        print("start_time_={}".format(start_time_))
                        print("end_time_={}".format(end_time_))

                        print("duration={}".format(duration))
                        k = LessonCompletionStats.objects.filter(
                            lesson=lesson,
                            user=user,
                            # start_date=start_time_,
                            # end_date=end_time_,
                            # duration=duration
                        )
                        if not k:
                            LessonCompletionStats.objects.get_or_create(
                                lesson=lesson,
                                user=user,
                                start_date=start_time_,
                                end_date=end_time_,
                                duration=duration
                            )
                        else:
                            #If the stats exists, update
                            k = k.last()
                            if k.end_date != end_time_ and k.duration != duration:
                                k.end_date=end_time_
                                k.duration=duration
                                k.save()
                        print("Created:{}".format(k))
                    # else:
                    #     #The whole lesson was not completed, bt we want to check if it was started
                    #     try:
                    #         if is_video is True:
                    #             start_time_ = video_start_date
                    #             # end_time_ = video_end_date
                    #         else:
                    #             start_time_ = min(min_start_times)
                    #             # end_time_ = max(max_end_times)
                    #         LessonsStartedStats.objects.get_or_create(
                    #             lesson=lesson,
                    #             user=user,
                    #             start_date=start_time_
                    #         )
                    #     except Exception as e:
                    #         print("Lesson started check error:", e)
                    try:
                        if is_video is True:
                            start_time_ = video_start_date
                            # end_time_ = video_end_date
                        else:
                            try:
                                start_time_ = min(min_start_times)
                            except Exception as e:
                                start_time_ = start_time_
                                print("start_time_ error:", e)
                            # end_time_ = max(max_end_times)
                        LessonsStartedStats.objects.get_or_create(
                            lesson=lesson,
                            user=user,
                            start_date=start_time_
                        )
                    except Exception as e:
                        print("Lesson started check error:", e)

                # createFileCache(file_path, users_list)
                return users_count, users_list


    def getUsersCompletedModule(self, module, start_date=None, end_date=None, create_recent_stats=False):
        users_completed_module_count = 0
        users_completed_module = []
        module_lessons = Lesson.objects.filter(
            category=module
        )

        users_in_lessons = []
        questions = Question.objects.filter(
            is_active=True
        )
        quests_tracking = QuestionTracking.objects.all()

        for module_lesson in module_lessons:
            # completed_count, users_completed = self.getUsersCompletedLesson(
            #     module_lesson, start_date, end_date, questions.filter(
            #         lesson=module_lesson
            #     ),quests_tracking, False
            # )
            completed_count, users_completed = self.getUsersCompletedLesson(
                module_lesson, start_date, end_date, questions.filter(
                    lesson=module_lesson
                ), quests_tracking, create_recent_stats
            )
            # create_recent_stats is by default false so as load existing summarised stats

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

        # return users_completed_module_count, users_completed_module
        users_completed_module = list(set(users_completed_module))
        return len(users_completed_module), users_completed_module














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

        try:
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)
            user_account_type = request.query_params.get('user_account_type', None)
            location = request.query_params.get('location', None)
            module_id = request.query_params.get('module', None)
            filter = request.query_params.get('filter', None)
        except Exception as e:
            start_date = request['start_date'] or None
            end_date = request['end_date'] or None
            user_account_type = request['user_account_type'] or None
            location = request['location'] or None
            module_id = request['module'] or None
            filter = request['filter'] or None

        if module_id is not None:
            modules = Category.objects.filter(id=module_id)
        else:
            modules = Category.objects.all()

        response  = []


        #total_users = request.query_params.get('total_users', None)
        try:
            month_or_week = request.query_params.get('month_or_week', None)
        except Exception as e:
            month_or_week = 'month'
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
        print("weeks_dates_in_period={}".format(weeks_dates_in_period))
        if filter == 'load_new_stats_users_number_per_module':
            print("START_DATE={}".format(start_date))
            print("END_DATE={}".format(end_date))
            create_recent_stats = True
            modules = Category.objects.all()
            for module in modules:
                response.append(
                    {
                        'module': '{}: {}'.format(module.order, module.name),
                        'total': self.getUsersCompletedModule(
                            module, start_date, end_date, create_recent_stats
                        )[0],
                    }
                )
        elif filter == 'users_number_per_module':
            print("START_DATE={}".format(start_date))
            print("END_DATE={}".format(end_date))
            for module in Category.objects.all():
                response.append(
                    {
                        'module': '{}: {}'.format(module.order, module.name),
                        'total': self.getUsersCompletedModule(module, start_date, end_date)[0],
                    }
                )
        elif filter == 'location_of_completing_modules':
            #Provide the filter=location_of_completing_modules and the location id

            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-07-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            locations = Location.objects.filter(is_active=True)

            users_completing_modules = []
            for module in Category.objects.all():
                # module = modules.last()
                users_completed = self.getUsersCompletedModule(module, start_date, end_date)[1]
                # users_completed = self.users.filter(
                #     id__in=[u.id for u in users_completed]
                # )
                users_completing_modules += [u.id for u in users_completed]

            for location in locations:
                response.append(
                    {
                        'location': location.name,
                        'count': self.users.filter(
                            location=location,
                            id__in=users_completing_modules
                        ).count()
                    }
                )
        elif filter == 'time_taken_to_complete_module':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            modules = Category.objects.all()
            for module in modules:
                users_completed = self.getUsersCompletedModule(module, start_date, end_date)[1]

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
                        ).order_by('-created').first()
                        start_time = start_time.data[0]['end_time']
                        print("Got here 3")

                        end_time = LesssonTracking.objects.filter(
                            lesson=module_last_lesson,
                            user=user
                        ).order_by('created').last().data[0]['end_time']

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
        elif filter == 'user_type_completing_modules':
            if start_date is None and end_date is None:
                start_date = request.query_params.get('start_date', '2020-05-01')
                end_date = request.query_params.get('end_date', str(datetime.now().date()))

            print("users_count0={}".format(users.count()))
            modules = Category.objects.all()
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

                individuals_count  = 0
                group_count = 0

                # users_completing = self.getUsersCompletedModule(modules.last(), start_date_, week_start_date)[1]

                users_all = []
                for module in modules:
                    users_completing = self.getUsersCompletedModule(module, start_date_, week_start_date)[1]
                    # users_completing = self.getUsersCompletedModule(module, start_date, end_date)[1]

                    users_all = users_all + [u.id for u in users_completing]
                    print("1:{}:{}=={}".format(module.order, module.name,len(users_all)))
                    print("users_completing={}".format(len(users_completing)))

                for u in self.users.filter(id__in=users_all):
                    if u.account_type == Choice.INDIVIDUAL:
                        individuals_count += 1
                    else:
                        group_count += 1

                response.append(
                    {   'week': week_start_date,#disp,
                        'data':{
                            'individual': individuals_count,
                            'group': group_count
                        }
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
