import pytz
from datetime import datetime
from dateutil.parser import parse
from lenga.settings.local import EXCLUDE_START_DATE
from lenga.settings.local import TEST_USERS_LIST
from data_tracking.models import ModuleQuestionsCompletedStats, QuestionTracking, UserCompletedModulesStats, \
    LessonCompletionStats
from learning.models import Lesson, Question, Category
from users.models import User


def time_to_eat(start_time, timezone="Africa/Nairobi"):
    timezone = "Africa/Nairobi"
    try:
        start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S.%f %z')
    except Exception as e:
        try:
            start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S+%z')
        except Exception as e:
            #2021-03-07 20:00:58+00:00
            try:
                dt = parse(str(start_time)) #2018-06-29 17:08:00.586525+00:00
                start_time = '{} {}'.format(str(dt.date()), dt.time()) #2018-06-29 17:08:00.586525
                start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S.%f')
                try:
                    start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S.%f')
                except Exception as e:
                    start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')

    utcmoment = start_time.replace(tzinfo=pytz.utc)
    localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
    start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

def loadModulesProgressStats(modules, users):

    for module in modules:

        lessons_in_module = Lesson.objects.filter(
            category=module
        )
        total_items_in_module = 0
        for lesson in lessons_in_module:
            questions_in_lesson = Question.objects.filter(
                lesson=lesson, is_active=True
            )
            for question in questions_in_lesson:
                total_items_in_module += 1
                question_tracker = QuestionTracking.objects.filter(
                    question=question
                )
                if question_tracker:
                    for user in users:
                        user_question_data = question_tracker.filter(
                            user=user
                        )
                        if user_question_data:
                            ModuleQuestionsCompletedStats.objects.create(
                                module=module,
                                lesson=lesson,
                                question=question,
                                user=user,
                                completion_date=question.created,
                            )

        for k in ModuleQuestionsCompletedStats.objects.all():
            k.total_items_in_module=total_items_in_module
            k.save()


def createUserCompletedModulesStats():
    print("Started at:{}".format(datetime.now()))
    modules = Category.objects.all()
    user_lessons_completed = LessonCompletionStats.objects.all()
    users = User.objects.filter(is_active=True).exclude(
        first_name__in=TEST_USERS_LIST
    ).exclude(created__date__lt=EXCLUDE_START_DATE)
    for user in users:
        print("User:{}".format(user.id))
        user_completed_modules = []
        for module in modules:
            # user_module_lessons_completed = user_lessons_completed.filter(
            #     lesson__category=module,
            #     user=user
            # )
            user_module_lessons_completed = user_lessons_completed.filter(
                lesson__category=module,
                user=user
            )#.order_by('lesson').distinct()
            ###


            ###
            module_lessons = Lesson.objects.filter(
                category=module
            )

            completed_lessons_count = user_module_lessons_completed.count()
            # if completed_lessons_count == module_lessons.count():
            if completed_lessons_count >= module_lessons.count():
                user_completed_modules.append(module)
                first_lesson_completed = user_module_lessons_completed.filter(
                    lesson__order=1
                ).last()
                last_lesson_completed = user_module_lessons_completed.filter(
                    lesson__order=module_lessons.count()
                ).last()

                start_time_ = first_lesson_completed.start_date
                end_time_ = last_lesson_completed.end_date
                start_time = time_to_eat(start_time_)
                end_time = time_to_eat(end_time_)
                diff_seconds = (end_time - start_time).total_seconds()
                UserCompletedModulesStats.objects.get_or_create(
                    user=user,
                    module=module,
                    start_date=first_lesson_completed.start_date,
                    completion_date=last_lesson_completed.end_date,
                    duration=diff_seconds
                )
    print("Completed at:{}".format(datetime.now()))