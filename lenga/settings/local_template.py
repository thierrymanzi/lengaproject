# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-21 17:41:23
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 11:47:32
# Project: lenga

DEBUG = True


ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

EMAIL_HOST = '<email host>'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'user email'
EMAIL_HOST_PASSWORD = 'password!'
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

SITE_HEADER = '<Default Site Header>'
