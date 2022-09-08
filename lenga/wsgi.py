# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-07-07 13:44:41
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-07-07 14:07:51
# Project: lenga
"""
WSGI config for lenga project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lenga.settings.base')

application = get_wsgi_application()
