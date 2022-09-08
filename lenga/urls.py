# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 20:51:03
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-07-07 14:31:41
# Project: lenga
"""lenga URL Configuration"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sites.models import Site
from django.urls import path, re_path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls

from lenga.router import url_patterns as router_patterns
from users.api.views import ListCreatePermissions, UpdatePermissionsView


try:
    site_header = Site.objects.get_current().name
except Exception:
    site_header = settings.SITE_HEADER

admin.site.site_header = site_header

# default error handlers
handler500 = 'rest_framework.exceptions.server_error'
handler400 = 'rest_framework.exceptions.bad_request'

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include_docs_urls(title="{} API Docs".format(site_header), public=False)),

    # Authentication
    re_path(r'api/v1/auth/app/$', obtain_auth_token),  # Mobile
    re_path(r'api/v1/auth/', include('oauth2_provider.urls',
                                 namespace='oauth2_provider')),  # Web

    # Permissions
    re_path(r'api/v1/permissions/$', ListCreatePermissions.as_view()),
    re_path(r'api/v1/permissions/(?P<id>[0-9a-z-]+)/$',
        UpdatePermissionsView.as_view()),

    # custom paths
    path('', include('users.urls')),
    path('', include('learning.urls')),
    path('', include('data_tracking.urls')),

    # dashboard
    path('', include('dashboard.urls')),
]

urlpatterns = urlpatterns + router_patterns

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    # removed in order to use AWS for media files
    # urlpatterns += static(settings.MEDIA_URL,
    #                       document_root=settings.MEDIA_ROOT)
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += staticfiles_urlpatterns()
