#!/projects/env/bin/python
###!/Users/elijah/.virtualenvs/lengaenv/bin/python
#####!/projects/env/bin/python
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
from dashboard.utils.modules_completion import BaseUptakeModuleCompletionStats




def time_to_eat(start_time, timezone="Africa/Nairobi"):
    timezone = "Africa/Nairobi"
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z')
    utcmoment = start_time.replace(tzinfo=pytz.utc)
    localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
    start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

def create_data():

    # users = User.objects.filter(is_active=True)
    print("Started at:{}".format(datetime.now()))

    modules = Category.objects.all()

    users = User.objects.filter(is_active=True).exclude(
                username__icontains='test'
            ).exclude(first_name__in=TEST_USERS_LIST).exclude(
                created__date__lt=EXCLUDE_START_DATE
            )

    request  = {}
    start_date = date(2020, 11, 1)
    end_date = datetime.now().date()
    request['start_date'] = str(start_date)
    request['end_date'] = str(end_date)
    request['filter'] = 'load_new_stats_users_number_per_module'
    request['user_account_type'] = None
    request['location'] = None
    request['module'] = None



    baseUptakeStats = BaseUptakeModuleCompletionStats(request, modules, users)


    print("GOT HERE")
    response = baseUptakeStats.getData()
    print("Ended at: {}".format(datetime.now()))



create_data()
