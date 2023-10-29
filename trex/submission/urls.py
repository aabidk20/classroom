from django.urls import path, include

from .views import (
    SubmissionListView,
)

app_name = "submission"

urlpatterns = [
    path('', SubmissionListView.as_view(), name='list'),
]
