from django.db.models import Count, F

from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from datetime import datetime, timedelta, date

from dashboard.utils.summarised.general_utils import get_no_partners, get_module_english_name
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


class BaseEngagementHandler:
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


    def get_queryset(self):
        # lessons_completed = TimeTakenOnModuleStat.objects.filter(
        #     # module=module_tracking.category,
        #     # user=module_tracking.user,
        #     # start_date=start_time,
        #     # end_date=end_time,
        #     # duration=diff_seconds
        #     start_date__gte = self.start_date,
        #     end_date__lte = self.end_date,
        # )
        # lessons_completed = LessonCompletionStats.objects.filter(
        #     start_date__gte=self.start_date,
        #     end_date__lte=self.end_date,
        # )
        # print("lessons_completed count={}".format(lessons_completed.count()))

        print("self.modules.count()={}".format(self.modules.count()))

        if self.modules.count() == 1:
            # If self.partners is not None, get here
            # lessons_completed = TimeTakenOnLessonStat.objects.filter(
            #     start_date__gte=self.start_date,
            #     end_date__lte=self.end_date,
            # )
            # lessons_completed = LessonCompletionStats.objects.filter(
            #     start_date__gte=self.start_date,
            #     end_date__lte=self.end_date,
            # )

            ####20210409###
            # lessons_completed = LessonCompletionStats.objects.filter(
            #     user__created__date__gte=self.start_date,
            #     user__created__date__lte=self.end_date,
            # )
            ####20210409###
            lessons_completed = LessonCompletionStats.objects.filter(
                start_date__date__gte=self.start_date,
                end_date__date__lte=self.end_date,
            )
            print("self.modules={}".format(self.modules))
            # users_list = []
            # k_ids = []
            # for k in lessons_completed:
            #     if k.user not in users_list:
            #         lessons_completed2 = lessons_completed.filter(
            #             lesson__category=self.modules.last(),
            #             lesson__in=self.lessons,
            #             id=k.id
            #         ) #.order_by('user').distinct()
            #         users_list.append(k.user)
            #         k_ids.append(k.id)
            # lessons_completed = lessons_completed.filter(id__in=k_ids)

            # lessons_completed = lessons_completed.filter(
            #     lesson__category=self.modules.last(),
            #     lesson__in=self.lessons
            # )


        else:
            ####20210409###
            # lessons_completed = UserCompletedModulesStats.objects.filter(
            #     user__created__date__gte=self.start_date,
            #     user__created__date__lte=self.end_date,
            # )
            ####20210409###
            lessons_completed = UserCompletedModulesStats.objects.filter(
                start_date__date__gte=self.start_date,
                completion_date__date__lte=self.end_date,
            )
        if self.partners:
            #If self.partners is not None, get here
            no_partners_ids, no_partners_ids_list = get_no_partners()
            if self.partners == 'no_partner':
                no_partner = Partner.objects.filter(id__in=no_partners_ids_list)
                allPartners = Partner.objects.filter(is_active=True).exclude(
                    id__in=no_partners_ids_list
                )
                self.partners = no_partner

                lessons_completed1 = lessons_completed.filter(
                    user__partner=None
                )
                lessons_completed = lessons_completed.filter(
                    user__partner__in=no_partner
                ) | lessons_completed1
            else:
                if self.partners == 'all':
                    self.partners = Partner.objects.filter(
                        is_active=True
                    ).exclude(
                    id__in=no_partners_ids_list
                )
                elif self.partners == 'all_partners_and_no_partner':
                    pass
                else:
                    lessons_completed = lessons_completed.filter(
                        user__partner__in=self.partners
                    )
        if self.locations:
            # print("self.locations={}".format(self.locations))
            lessons_completed = lessons_completed.filter(
                user__location__in=self.locations
            )
        if self.user_type:
            # print("self.user_type={}".format(self.user_type))
            lessons_completed = lessons_completed.filter(
                user__account_type__in=self.user_type
            )
        lessons_completed = lessons_completed.filter(
            user__in=self.users
        )

        print("lessons_completed count={}".format(lessons_completed.count()))

        self.queryset = lessons_completed


    def getSummaryStats(self):
        """
        If any of the filters gets here as None,
        it means select all items in that filter/do
        not add the filter
        """
        response = []
        self.get_queryset()

        if self.modules.count() > 1:
            for module in self.modules:
                data = self.queryset.filter(
                    module=module
                )
                total_time_spent = data.aggregate(Sum('duration'))['duration__sum'] or 0
                print("total_time_spent={}".format(total_time_spent))
                total_time_spent = total_time_spent / 60
                users_count = data.order_by('user').distinct().count()
                print("users_count={}".format(users_count))

                total_users = users_count if users_count > 0 else 1
                average_time = total_time_spent / total_users

                module_eng_name = get_module_english_name(module.order)
                response.append(
                    {
                        # 'module': '{}: {}'.format(module.order, module.name),
                        'module': '{}: {}'.format(module.order, module_eng_name),
                        'time_taken': round(average_time, 2)
                     }
                )
        else:
            print("HERE")
            print("Lessons={}".format(self.lessons))
            for lesson in self.lessons:
                print("QSET={}".format( self.queryset.count()))
                data = self.queryset.filter(
                    lesson=lesson
                )

                total_time_spent = data.aggregate(Sum('duration'))['duration__sum'] or 0
                total_time_spent = total_time_spent / 60
                users_count = data.order_by('user').distinct().count()

                total_users = users_count if users_count > 0 else 1
                average_time = total_time_spent / total_users

                response.append(
                    {'lesson': '{}: {}'.format(lesson.order, lesson.description),
                     'time_taken': round(average_time, 2)
                     }
                )

        return response


