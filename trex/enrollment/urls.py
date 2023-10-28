from django.urls import path, include

from .views import (
    EnrollmentListView,
)

app_name = "enrollment"

urlpatterns = [
    path('', EnrollmentListView.as_view(), name='list'),
    # path('create/', EnrollmentCreateView.as_view(), name='create'),
]
