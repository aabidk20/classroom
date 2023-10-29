from django.urls import path, include

from .views import (
    SubmissionListView,
    SubmissionCreateView,
    SubmissionUpdateView,
    SubmissionDeleteView,
)

app_name = "submission"

urlpatterns = [
    path('', SubmissionListView.as_view(), name='list'),
    path('create/', SubmissionCreateView.as_view(), name='create'),
    path('<int:submission_id>/update/', SubmissionUpdateView.as_view(), name='update'),
    path('<int:submission_id>/delete/', SubmissionDeleteView.as_view(), name='delete'),
]
