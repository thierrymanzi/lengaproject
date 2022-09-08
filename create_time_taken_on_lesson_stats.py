#!/projects/env/bin/python
import os
import sys



sys.path.append("/api/lenga")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lenga.settings.base")

import django

django.setup()


import pytz
from datetime import datetime
from learning.models import Lesson
from users.models import User
from data_tracking.models import LesssonTracking, TimeTakenOnLessonStat


def time_to_eat(start_time, timezone="Africa/Kigali"):
    timezone = "Africa/Kigali"
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z')
    utcmoment = start_time.replace(tzinfo=pytz.utc)
    localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
    start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')


def createTimeTakenOnLesson():
    lessons_tracking = LesssonTracking.objects.filter(created__date__gte='2020-09-01')
    i = 0
    print("STARTED AT: {}".format(datetime.now()))
    lessons = Lesson.objects.all()
    users = User.objects.filter(is_active=True)
    for user in users:
        for lesson in lessons:
            try:
                data = lessons_tracking.filter(
                    lesson=lesson, user=user
                )
                all = []
                for k in data:
                    for w in k.data:
                        print("w={}".format(w['end_time']))
                        try:
                            print("w.data['end_time']={}".format(w['end_time']))
                            print("type={}".format(type(w['end_time'])))
                            all.append(time_to_eat(w['end_time']))
                        except Exception as e:
                            print("Error |||:{}:{}".format(k.id, e))

                first_item_end_time = min(all)
                last_item_end_time = max(all)



                start_time = first_item_end_time #time_to_eat(first_item_end_time)
                end_time = last_item_end_time #time_to_eat(last_item_end_time)
                diff_seconds = (end_time - start_time).total_seconds()

                curr = TimeTakenOnLessonStat.objects.get_or_create(
                    lesson=lesson,
                    user=user,
                    start_date=start_time,
                    end_date=end_time,
                    duration=diff_seconds
                )
                i += 1
                print("Created:{}".format(i))
            except Exception as e:
                pass

    print("ENDED AT: {}".format(datetime.now()))

createTimeTakenOnLesson()