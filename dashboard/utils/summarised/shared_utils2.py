from datetime import datetime
from data_tracking.models import (
    QuestionTracking,
    LessonCompletionStats,
    LesssonTracking
)
from learning.models import Lesson, Question


class CompletionSharedUtil:
    def __init__(self, module, lesson, start_date, end_date, users, lessons_completed, questions, quests_tracking, periodDetails):
        self.module = module
        self.lesson = lesson
        self.start_date = start_date
        self.end_date = end_date
        self.users = users
        self.lessons_completed = lessons_completed
        self.questions = questions
        self.quests_tracking = quests_tracking
        self.periodDetails = periodDetails
        self.create_recent_stats = False


    def getUsersCompletedModule(self):
        users_completed_module_count = 0
        users_completed_module = []
        module_lessons = Lesson.objects.filter(
            category=self.module
        )

        users_in_lessons = []
        # questions = Question.objects.filter(
        #     is_active=True
        # )
        # quests_tracking = QuestionTracking.objects.all()
        questions = self.questions
        quests_tracking = self.quests_tracking

        for module_lesson in module_lessons:
            completed_count, users_completed, lession_duration_list = self.getUsersCompletedLesson(
                module_lesson,
                self.start_date,
                self.end_date, questions.filter(
                    lesson=module_lesson
                ),
                quests_tracking,
                self.lessons_completed,
                False#self.create_recent_stats
            )
            # create_recent_stats is by default false so as load existing summarised stats

            users_in_lessons.append(
                {
                    'lesson': module_lesson,
                    'users': users_completed,
                    'lesson_duration': lession_duration_list
                }
            )

        for user in self.users:
            lesson_completion_appearance_count = 0
            for user_in_lesson in users_in_lessons:
                if user in user_in_lesson['users'] and self.module == user_in_lesson['lesson'].category:
                    lesson_completion_appearance_count += 1
            if lesson_completion_appearance_count == module_lessons.count():
                users_completed_module_count += 1
                users_completed_module.append(user)

        # return users_completed_module_count, users_completed_module
        users_completed_module = list(set(users_completed_module))
        return len(users_completed_module), users_completed_module


    def getUsersCompletedLesson(
            self, lesson, start_date, end_date, module_questions,
            quests_tracking, lessons_completed, create_stats_data
    ):
        users_count = 0
        users_list = []
        duration_list = []

        # lessons_completed = LessonCompletionStats.objects.filter(
        #     start_date__gte=start_date,
        #     end_date__lte=end_date,
        #     lesson=lesson
        # )
        lessons_completed = lessons_completed.filter(
            lesson=lesson
        )
        if create_stats_data is False:
            print("GOT HERE")
            if lessons_completed:
                print("GOT HERE 2")
                users_list = []
                for lesson_completed in lessons_completed:
                    users_list.append(lesson_completed.user)
                    duration_list.append(lesson_completed.duration)
                users_list = list(set(users_list))
                return len(users_list), users_list, duration_list
            else:
                print("GOT HERE 3")
                return 0, [], [0,0]
        else:
            if create_stats_data is True: #To create new
                print("HERE 2_1")
                lesson_questions = module_questions.filter(
                    lesson=lesson, is_active=True
                )


                quests_responses = quests_tracking.filter(
                    question__in=[q for q in lesson_questions]
                )


                for user in self.users:
                    user_completed_questions = []
                    # user_quests_responses = quests_responses.filter(
                    #     user=user
                    # )
                    lesson_trackings = LesssonTracking.objects.filter(
                        lesson=lesson,
                    ).order_by('created')



                    min_start_times = []
                    max_end_times = []
                    for lesson_question in lesson_questions:
                        user_quests_responses = quests_responses.filter(
                            question=lesson_question, user=user
                        )
                        if user_quests_responses:

                            if start_date is not None and end_date is not None:
                                lesson_trackings = lesson_trackings.filter(
                                    user=user
                                )

                                if lesson_trackings:
                                    for lesson_tracking in lesson_trackings:
                                        # lesson_tracking = lesson_tracking.last()
                                        endTime = lesson_tracking.data[0]['end_time']
                                        endTime_ = self.periodDetails.time_to_eat(endTime)
                                        endTime = endTime_.date()
                                        start_date = datetime.strptime(str(start_date), "%Y-%m-%d").date()
                                        try:
                                            end_date = datetime.strptime(str(end_date), "%Y-%m-%d").date()
                                        except Exception as e:
                                            end_date = datetime.strptime(str(end_date), "%Y-%m-%d %H:%M:%S").date()
                                        if endTime >= start_date and endTime <= end_date:
                                            user_completed_questions.append(lesson_question)
                                            min_start_times.append(endTime_)
                                            max_end_times.append(endTime_)
                            # else:
                            #     user_completed_questions.append(lesson_question)




                    user_completed_questions = list(set(user_completed_questions))
                    if len(user_completed_questions) == lesson_questions.count():
                        print("Before creation")
                        users_count += 1
                        users_list.append(user)
                        user_completed_questions.append(lesson_question)
                        start_time_ = min(min_start_times)
                        end_time_ = max(max_end_times)
                        print("start_time_={}".format(start_time_))
                        print("end_time_={}".format(end_time_))
                        duration = (end_time_ - start_time_).total_seconds() / 60
                        duration_list.append(duration)
                        print("duration={}".format(duration))
                        k = LessonCompletionStats.objects.filter(
                            lesson=lesson,
                            user=user,
                            start_date=start_time_,
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

                # createFileCache(file_path, users_list)
                return users_count, users_list, duration_list





