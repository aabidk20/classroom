from django.urls import path, include
from .views import (
    AssignmentListView,
    AssignmentCreateView,
    AssignmentDetailView,
)

app_name = "assignment"

urlpatterns = [
    path('', AssignmentListView.as_view(), name='list'),
    path('create/', AssignmentCreateView.as_view(), name='create'),
    path('<int:assignment_id>/', AssignmentDetailView.as_view(), name='detail'),
]
