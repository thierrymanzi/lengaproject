# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2019-07-11 16:18:42
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-07-07 14:09:53
# Project: bolt

import sentry_sdk

from django.conf import settings

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.utils import BadDsn

try:
    if not settings.DEBUG:
        sentry_sdk.init(
            dsn="https://{}@sentry.io/1458838".format(settings.SENTRY_KEY),
            integrations=[DjangoIntegration()]
        )

except BadDsn:
    pass
