#!/projects/env/bin/python
####!/Users/elijah/.virtualenvs/lengaenv/bin/python
#####!/projects/env/bin/python
import os
import sys


# sys.path.append("/Users/elijah/Projects/LENGA/backend/live20201102/lenga")
sys.path.append("/api/lenga")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lenga.settings.base")

import django

django.setup()

from dashboard.utils.progress_through_modules_cache import createUserCompletedModulesStats


def create_data():
    createUserCompletedModulesStats()



create_data()
