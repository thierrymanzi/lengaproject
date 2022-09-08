from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status


from datetime import datetime, timedelta, date

from dashboard.utils.summarised.general_utils import get_no_partners, get_module_english_name
from dashboard.utils.summarised.period_utils import PeriodUtils
from dashboard.utils.summarised.shared_utils import CompletionSharedUtil
from dashboard.utils.summarised.signup.breakdown_utils.all import getBreakdownByAll
from dashboard.utils.summarised.signup.breakdown_utils.location import getBreakdownByLocation
from dashboard.utils.summarised.signup.breakdown_utils.partners import getBreakdownByPartners
from dashboard.utils.summarised.signup.breakdown_utils.period import getBreakdownByPeriod
from dashboard.utils.summarised.signup.breakdown_utils.user_type import getBreakdownByUserType
from data_tracking.models import LesssonTracking, LessonCompletionStats, QuestionTracking, UserCompletedModulesStats, \
    LessonsStartedStats, ModulesStartedStats
from utils.choices import Choice as choice
from users.models import User
from learning.models import Location, Lesson, Question, Partner


class BaseLessonsStartedHandlerHandler:
    def __init__(
            self, request, users, period_type, partners,
            locations, user_type, start_date, end_date,
            breakdown_item, modules, lessons
    ):
        period_type = period_type if period_type is\
                                     not None else choice.MONTH
        period_type = period_type.capitalize()
        self.request = request
        self.users = users
        self.partners = partners
        self.locations = locations
        self.user_type = user_type
        self.start_date = start_date
        self.end_date = end_date
        self.period_details = PeriodUtils(
            period_type, start_date, end_date
        )
        self.breakdown_item = breakdown_item.lower()
        self.modules = modules
        self.lessons = lessons
        self.create_recent_stats = False


    def get_queryset(self):
        lessons_completed = LessonCompletionStats.objects.filter(
            start_date__gte=self.start_date,
            end_date__lte=self.end_date,
            #user__created__date__gte=self.start_date,
            #user__created__date__lte=self.end_date,
        )
        print("self.start_date={}".format(self.start_date))
        print("self.end_date={}".format(self.end_date))
        print("lessons_completed count={}".format(lessons_completed.count()))
        print("total_users={}".format(self.users.count()))

        if self.partners:
            #If self.partners is not None, get here
            no_partners_ids, no_partners_ids_list = get_no_partners()
            if self.partners == 'no_partner':
                no_partner = Partner.objects.filter(
                    id__in=no_partners_ids_list,
                    is_active=True
                )
                # allPartners = Partner.objects.filter(is_active=True)
                lessons_completed1 = lessons_completed.filter(
                    user__partner__in=no_partner
                )

                lessons_completed2 = lessons_completed.filter(
                    user__partner=None
                )

                lessons_completed = lessons_completed1 | lessons_completed2

                # self.partners = no_partner
            else:
                if self.partners == 'all':
                    self.partners = Partner.objects.filter(
                        is_active=True
                    ).exclude(id__in=no_partners_ids_list)

                    lessons_completed = lessons_completed.exclude(
                        user__partner__id__in=no_partners_ids_list
                    ).exclude(user__partner=None)
                elif self.partners == 'all_partners_and_no_partner':
                    pass
                else:
                    lessons_completed = lessons_completed.filter(
                        user__partner__in=self.partners
                    )
        if self.locations:
            lessons_completed = lessons_completed.filter(
                user__location__in=self.locations
            )
        if self.user_type:
            lessons_completed = lessons_completed.filter(
                user__account_type__in=self.user_type
            )
        # self.users = self.users.filter(
        #     id__in=list(set([lc.user.id for lc in lessons_completed]))
        # )

        print("lessons_completed count={}".format(lessons_completed.count()))
        self.lessons_completed = lessons_completed

        self.queryset = lessons_completed

    # def getUsersCompletedModule(self, engagementSharedUtil):
    #     module = engagementSharedUtil.module
    #     module_lessons = Lesson.objects.filter(
    #         category=module
    #     )
    #     lessons_count = module_lessons.count()
    #     i = 0
    #     lesson_users = {}
    #     for lesson in module_lessons:
    #         completed_count, users_completed, lession_duration_list = \
    #             engagementSharedUtil.getUsersCompletedLesson(
    #                 lesson, self.start_date, self.end_date,
    #                 engagementSharedUtil.questions.filter(
    #                     lesson=lesson
    #                 ),
    #                 engagementSharedUtil.quests_tracking,
    #                 self.lessons_completed, self.create_recent_stats
    #             )
    #         lesson_users[i] = list(set(users_completed))
    #         i += 1
    #
    #     user_appearances = []
    #     for key, users_for_lesson in lesson_users.items():
    #         for user in users_for_lesson:
    #             user_appearances.append(user)
    #     return [u for u in user_appearances if user_appearances.count(u) == lessons_count]



    def getUsersStartedLesson(self, module=None, lesson=None): #engagementSharedUtil):
        if module is not None:
            # completions = LessonsStartedStats.objects.filter(
            #     lesson__category=module,
            #     start_date__date__gte=self.start_date
            # )
            completions = ModulesStartedStats.objects.filter(
                module=module,
                start_date__date__gte=self.start_date
            )
        if lesson is not None:
            completions = LessonsStartedStats.objects.filter(
                lesson=lesson,
                start_date__date__gte=self.start_date
            )

        print("self.partners={}".format(self.partners))
        print('completions4_1={}'.format(completions))
        if self.partners:
            #If self.partners is not None, get here
            print("self.partners2={}".format(self.partners))
            no_partners_ids, no_partners_ids_list = get_no_partners()
            if self.partners == 'no_partner':
                print("self.partners={}".format(self.partners))
                noPartners = Partner.objects.filter(
                    is_active=True,
                    id__in=no_partners_ids_list
                )
                completions1 = completions.filter(
                    user__partner=None
                )
                completions = completions.filter(
                    user__partner__in=noPartners
                ) | completions1
                print("no_partner_completions={}".format(completions))

            else:
                if self.partners == 'all':
                    self.partners = Partner.objects.filter(
                        is_active=True
                    ).exclude(
                    id__in=no_partners_ids_list)

                    completions = completions.filter(
                        user__partner__in=self.partners
                    )
                elif self.partners == 'all_partners_and_no_partner':
                    pass
                else:
                    completions = completions.filter(
                        user__partner__in=self.partners
                    )
        if self.locations:
            completions = completions.filter(
                user__location__in=self.locations
            )
        if self.user_type:
            completions = completions.filter(
                user__account_type__in=self.user_type
            )

        return list(set([u.user for u in completions]))




    def getSummaryStats(self):
        """
        If any of the filters gets here as None,
        it means select all items in that filter/do
        not add the filter
        """
        response = []
        self.get_queryset()

        questions = Question.objects.filter(
            is_active=True
        )
        quests_tracking = QuestionTracking.objects.all()

        print("USERS ALL1={}".format(self.users.count()))
        engagementSharedUtil = CompletionSharedUtil(
            None, [], self.start_date, self.end_date,  # self.lessons for []
            self.users, self.queryset, questions, quests_tracking, self.period_details
        )

        total_users = self.users.count()
        total_users = total_users if total_users > 0 else 1
        print("USERS ALL2={}".format(total_users))

        if self.modules.count() > 1:
            users_completed_full_app = []
            app_modules_list = {}
            j = 0
            for module in self.modules:
                engagementSharedUtil.module = module

                users_completed = list(set(self.getUsersStartedLesson(module=module)))
                app_modules_list[j] = users_completed
                j += 1

                users_completed = len(users_completed)
                print("USERS COMPLETED HERE = {}".format(users_completed))
                module_eng_name = get_module_english_name(module.order)#[0:13]
                response.append(
                    {
                        # 'module': '{}: {}'.format(module.order, module.name),
                        'module': '{}: {}'.format(module.order, module_eng_name),
                        # 'percentage_users_completed': round(average_percentage, 2)
                        'percentage_users_completed': users_completed
                     }
                )
            # Get users who completed all lessons in the module
            # for user in self.users:
            #     user_modules = []
            #     for key, item in app_modules_list.items():
            #         if user in item:
            #             # users_completed_full_app.append(user)
            #             user_modules.append(user)
            #     if len(user_modules) == self.modules.count():
            #         users_completed_full_app.append(user)

            # full_module_average_percentage = (len(list(set(users_completed_full_app))) / total_users) * 100
            # print("users_completed_full_app={}".format(users_completed_full_app))
            # print("total_users={}".format(total_users))
            # response.append(
            #     {
            #         'module': 'Full app',
            #         # 'percentage_users_completed': round(full_module_average_percentage, 2)
            #         'percentage_users_completed': users_completed_full_app
            #     }
            # )

        else:
            users_completed_module = []#0
            module_lessons_list = {}
            module_lessons = self.lessons
            engagementSharedUtil.module = self.modules.last()
            i = 0
            for lesson in module_lessons:
                users_completed = len(list(set(self.getUsersStartedLesson(lesson=lesson))))

                print("USERS COMPLETED = {}".format(users_completed))
                module_lessons_list[i] = users_completed

                i += 1

                response.append(
                    {
                        'lesson': '{}: {}'.format(lesson.order, lesson.description),
                        'percentage_users_completed': users_completed
                     }
                )
            #Get users who completed all lessons in the module
            # users_started_module = list(set(self.getUsersStartedLesson(module=lesson.category)))

            # response.append(
            #     {
            #         'lesson': 'Full module',
            #         'percentage_users_completed': len(users_started_module)
            #      }
            # )
        return response
