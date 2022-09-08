from django.urls import path, re_path

from .views import (
    DashboardView,
    UserSignUpStatsView,
    UserModuleCompletionStatsView,
    UserLessonsCompletionStatsView,
    UsageSessionDurationStatsView,
    ProgressStatsView
)

from . import signup_views
from . import engagement_views
from . import completion_views
from . import export_all_views
from . import lessons_started_views


urlpatterns = [
    path('api/v1/dashboard/', DashboardView.as_view()),
    path('api/v1/dashboard/users/', UserSignUpStatsView.as_view()),
    path('api/v1/dashboard/modules-completion/', UserModuleCompletionStatsView.as_view()),
    path('api/v1/dashboard/lessons-completion/', UserLessonsCompletionStatsView.as_view()),
    path('api/v1/dashboard/usage/session-duration-total/', UsageSessionDurationStatsView.as_view()),
    path('api/v1/dashboard/progress/', ProgressStatsView.as_view()),
    path('api/v1/dashboard/signup/', signup_views.UserSignUpStatsView.as_view()),
    path('api/v1/dashboard/engagement/', engagement_views.EngagementStatsView.as_view()),
    path('api/v1/dashboard/completion/', completion_views.CompletionStatsView.as_view()),
    path('api/v1/dashboard/lessons-started/', lessons_started_views.LessonsStartedStatsView.as_view()),
    path('api/v1/dashboard/export-all/', export_all_views.ExportAllStatsView.as_view()),
]