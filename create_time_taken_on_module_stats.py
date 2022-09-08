#!/projects/env/bin/python
import os
import sys



sys.path.append("/api/lenga")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lenga.settings.base")

import django

django.setup()

import pytz
from datetime import datetime
from data_tracking.models import TimeTakenOnModuleStat, CategoryTracking


def time_to_eat(start_time, timezone="Africa/Kigali"):
    timezone = "Africa/Kigali"
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z')
    utcmoment = start_time.replace(tzinfo=pytz.utc)
    localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
    start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')


def createTimeTakenOnModule():
    modules_tracking = CategoryTracking.objects.filter(
    created__date__gte = '2020-09-01'
    )
    i = 0
    print("STARTED AT: {}".format(datetime.now()))
    print("Count={}".format(modules_tracking.count()))
    all = []
    for module_tracking in modules_tracking:
        try:
            modules_data = module_tracking.data#

            for module_data in modules_data:
                start_time_ = module_data['start_time']
                end_time_ = module_data['end_time']
                start_time = time_to_eat(start_time_)
                end_time = time_to_eat(end_time_)

                diff_seconds = (end_time - start_time).total_seconds()
                curr = TimeTakenOnModuleStat.objects.get_or_create(
                    module=module_tracking.category,
                    user=module_tracking.user,
                    start_date=start_time,
                    end_date=end_time,
                    duration=diff_seconds
                )
                all.append(curr)
                i += 1
            print("Created: {}".format(i))
        except Exception as e:
            print("Error:{}:{}".format(module_tracking.category.order, e))
    print("ENDED AT: {}".format(datetime.now()))


createTimeTakenOnModule()