#!/projects/env/bin/python
###!/Users/elijah/.virtualenvs/lengaenv/bin/python
import os
import sys


# sys.path.append("/Users/elijah/Projects/LENGA/backend/live20201102/lenga")


sys.path.append("/api/lenga")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lenga.settings.base")

import django

django.setup()

import pytz
from datetime import date, datetime
from lenga.settings.local import EXCLUDE_START_DATE
from lenga.settings.local import TEST_USERS_LIST
from users.models import User
from learning.models import Category
from data_tracking.models import LessonsStartedStats, ModulesStartedStats




def time_to_eat(start_time, timezone="Africa/Kigali"):
    timezone = "Africa/Kigali"
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z')
    utcmoment = start_time.replace(tzinfo=pytz.utc)
    localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
    start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

def create_data():

    modules = Category.objects.all()
    users = User.objects.filter(is_active=True).exclude(
        username__icontains='test'
    ).exclude(first_name__in=TEST_USERS_LIST).exclude(
        created__date__lt=EXCLUDE_START_DATE
    )
    for user in users:
        for module in modules:
            started_lessons = LessonsStartedStats.objects.filter(
                lesson__category=module, user=user
            ).exclude(
                    user__username__icontains='test'
                ).exclude(user__first_name__in=TEST_USERS_LIST).exclude(
                    created__date__lt=EXCLUDE_START_DATE
                )
            if started_lessons:
                start_times_list = []
                for sl in started_lessons:
                    start_times_list.append(sl.start_date)
                start_date = min(start_times_list)
                try:
                    ModulesStartedStats.objects.get_or_create(
                        module=module,
                        user=user,
                        start_date=start_date
                    )
                except Exception as e:
                    print("Module started check error:", e)


create_data()
