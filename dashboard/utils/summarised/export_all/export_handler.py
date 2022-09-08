import csv
from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum


from datetime import datetime, timedelta, date

from dashboard.utils.progress.email_utils import send_email
from dashboard.utils.summarised.period_utils import PeriodUtils
from dashboard.utils.summarised.shared_utils import CompletionSharedUtil
from dashboard.utils.summarised.signup.breakdown_utils.all import getBreakdownByAll
from dashboard.utils.summarised.signup.breakdown_utils.location import getBreakdownByLocation
from dashboard.utils.summarised.signup.breakdown_utils.partners import getBreakdownByPartners
from dashboard.utils.summarised.signup.breakdown_utils.period import getBreakdownByPeriod
from dashboard.utils.summarised.signup.breakdown_utils.user_type import getBreakdownByUserType
from data_tracking.models import LesssonTracking, LessonCompletionStats, QuestionTracking, TimeTakenOnModuleStat, \
    TimeTakenOnLessonStat, UserCompletedModulesStats
from utils.choices import Choice as choice
from users.models import User
from learning.models import Location, Lesson, Question, Partner


class BaseExportAllHandler:
    def __init__(
            self, request, users, start_date, end_date,
            modules, lessons, emailTo
    ):
        self.request = request
        self.users = users
        self.emailTo = emailTo

        self.start_date = start_date
        self.end_date = end_date
        self.period_details = PeriodUtils(
            'Month', start_date, end_date
        )
        self.modules = modules
        self.lessons = lessons


    def get_queryset(self):
        lessons_completed = TimeTakenOnModuleStat.objects.filter(
            start_date__gte = self.start_date,
            end_date__lte = self.end_date,
        )
        modules_completed = UserCompletedModulesStats.objects.filter(
            user__created__date__gte=self.start_date,
            user__created__date__lte=self.end_date,
        )
        print("lessons_completed count={}".format(lessons_completed.count()))

        print("self.modules.count()={}".format(self.modules.count()))

        self.lessons_completed = lessons_completed
        self.modules_completed = modules_completed


    def getVideoTimesTaken(self, lesson, user_video_responses1):
        no_of_times_taken = 0
        is_video = []
        question = Question.objects.filter(
            lesson=lesson, is_active=True,
            question_type='video'
        )
        if question:
            is_video.append(1)
            video_question = question.last()
            user_video_responses1 = user_video_responses1.filter(
                lesson=lesson
            )

            if user_video_responses1:
                # quest_video_tracking = user_quests_responses
                found_item = False
                found_item2 = False
                if user_video_responses1:
                    for video_data in user_video_responses1:
                        for data_item in video_data.data:
                            try:
                                if data_item['question_id'] == str(video_question.id) and data_item['type'] == 'ENDED':
                                    print("{}".format(data_item))
                                    startTime_ = self.time_to_eat(str(data_item['startTime']))
                                    endTime_ = self.time_to_eat(str(data_item['endTime']))
                                    startTime = startTime_.date()
                                    endTime = endTime_.date()

                                    is_video = True
                                    video_start_date = startTime_
                                    video_duration = (endTime_ - startTime_).total_seconds()
                                    print("video_duration={}".format(video_duration))
                                    found_item = True
                                    no_of_times_taken += 1
                                if found_item is True:
                                    found_item2 = True
                                    break
                            except Exception as e:
                                pass
                                # print("Errror:{}".format(e))
                        if found_item2 is True:
                          break
        is_video = True if len(is_video) > 1 else False
        return is_video, no_of_times_taken


    def getDetailedUserModuleCompletedLessons(
                    self, user, module
                ):
        lessons_completed = LessonCompletionStats.objects.filter(
            user=user,
            lesson__category=module,
            # user__created__date__gte=self.start_date,
            # user__created__date__lte=self.end_date,
        )

        lesson_tracking = LesssonTracking.objects.filter(
            user=user
        )

        lessons_completed_list = []
        lessons_checked = []
        for lesson_completed in lessons_completed:
            if lesson_completed.lesson not in lessons_completed_list:
                is_video, no_times = self.getVideoTimesTaken(lesson_completed.lesson, lesson_tracking)
                no_of_times_taken = lesson_tracking.filter(
                    lesson=lesson_completed.lesson
                ).count()
                no_of_times_taken = no_times if is_video is True else no_of_times_taken
                if lesson_completed.duration > 0 and no_of_times_taken == 0:
                    no_of_times_taken = 1
                lessons_completed_list.append({
                    'lesson': lesson_completed.lesson,
                    'time_of_completion': lesson_completed.end_date,
                    'duration': lesson_completed.duration,
                    'no_of_times_taken': no_times if is_video is True else no_of_times_taken

                })
                lessons_checked.append(lesson_completed.lesson)

        return lessons_completed_list




    def export(self):
        response = []
        email = self.emailTo
        print("START DATE = {}".format(self.start_date))
        print("END DATE = {}".format(self.end_date))

        # labels = ["username","ureal_username", "user_type", "location", "created"]
        labels = ["username", "user_type", "location", "created"]
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
            # user_details['real_username'] = user.username  # user.username
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
                lessons_completed = self.getDetailedUserModuleCompletedLessons(
                    user, module
                )
                completed_lessons_list = [lesson1['lesson'] for lesson1 in lessons_completed]
                # data.append(module.name)
                module_lessons = Lesson.objects.filter(category=module)
                for curr_module_lesson in module_lessons:
                    less = None
                    for lesson in lessons_completed:
                        print(lesson)
                        lesson_ = lesson['lesson']
                        if curr_module_lesson in completed_lessons_list and lesson_ == curr_module_lesson:  # == lesson1:
                            lesson_name = '{}: {}'.format(lesson_.description, lesson_.order)
                            lesson_name = 'Completed'

                            duration = lesson['duration']
                            try:
                                duration = float(duration)
                            except Exception as e:
                                print("DURETION ERRROR:{}:{}:{}".format(user.id, lesson.id, e))
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
                        data.append(round((duration/60), 2))
                        data.append(str(time_of_completion)[0:16])
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
        send_email(self.start_date, self.end_date, file_link, email)


    def getSummaryStats(self):
        """
        If any of the filters gets here as None,
        it means select all items in that filter/do
        not add the filter
        """
        response = []
        self.get_queryset()

        self.export()

        response.append({'message': 'Export will be sent to your email'})
        return response

