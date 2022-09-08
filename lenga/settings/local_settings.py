# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-07-07 13:29:29
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-07-07 14:34:43
# Project: lenga

DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'HOST': '<127.0.0.1>',
#         'NAME': '<lenga>',
#         'PASSWORD': '<lenga>',
#         'PORT': 5432,
#         'USER': '<postgres>',
#         'ATOMIC_REQUESTS': True,
#     }
# }


# ALLOWED_HOSTS = ['.busara.io']
# CORS_ORIGIN_WHITELIST = [ 'http://lenga.busara.io' ]

EMAIL_HOST = '<email host>'
EMAIL_PORT = 587
EMAIL_HOST_USER = '<user email>'
EMAIL_HOST_PASSWORD = '<password!>'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = '<default from email>'

SERVER_EMAIL = '<server email>'

# declare admins
ADMINS = (
    ('<sample admin name>', '<sample-admin-emai@email.em>'),
)
MANAGERS = ADMINS

# TIMEZONE
TIME_ZONE = 'UTC'

SITE_HEADER = 'Lenga'

SENTRY_KEY = 'some key'

FCM_SERVER_KEY = 'some key'
