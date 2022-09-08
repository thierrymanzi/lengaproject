#!/Users/elijah/.virtualenvs/lengaenv/bin/python
#####!/projects/env/bin/python
import os
import sys



#sys.path.append("/Users/elijah/Projects/LENGA/backend/live20201102/lenga")
sys.path.append("/api/lenga")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lenga.settings.base")

import django

django.setup()

import pytz
from datetime import datetime
from data_tracking.models import CategoryTrackingStats, CategoryTracking
from users.models import User


def time_to_eat(start_time, timezone="Africa/Kigali"):
    timezone = "Africa/Kigali"
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z')
    utcmoment = start_time.replace(tzinfo=pytz.utc)
    localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
    start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

# def create_data():
#
#     users = User.objects.filter(is_active=True)
#     category_trackings = CategoryTracking.objects.filter(
#         user__in=users
#     )
#     for category_tracking in category_trackings:
#         CategoryTrackingStats.objects.get_or_create(
#             module=category_tracking.category,
#             user=category_tracking.user,
#             start_date=time_to_eat(category_tracking.data[0]['start_time']),
#             completion_date=time_to_eat(category_tracking.data[0]['end_time'])
#         )
def create_data():

    users = User.objects.filter(is_active=True)
    print("Users loaded:{}".format(users.count()))
    category_trackings = CategoryTracking.objects.filter(
        user__in=users
    )
    print("category_trackings:{}".format(category_trackings.count()))
    for category_tracking in category_trackings:
        print("Working on:{}".format(category_tracking.id))
        try:
            CategoryTrackingStats.objects.get_or_create(
                module=category_tracking.category,
                user=category_tracking.user,
                start_date=time_to_eat(category_tracking.data[0]['start_time']),
                completion_date=time_to_eat(category_tracking.data[0]['end_time'])
            )
        except Exception as e:
            print("Error:{}::{}".format(category_tracking.id, e))

create_data()