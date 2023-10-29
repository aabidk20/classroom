from django.urls import path, include
from .views import (
    AssignmentListView,
    AssignmentCreateView,
    AssignmentDetailView,
    AssignmentUpdateView,
    AssignmentDeleteView,
)

app_name = "assignment"

urlpatterns = [
    path('', AssignmentListView.as_view(), name='list'),
    path('create/', AssignmentCreateView.as_view(), name='create'),
    path('<int:assignment_id>/', AssignmentDetailView.as_view(), name='detail'),
    path('<int:assignment_id>/update/', AssignmentUpdateView.as_view(), name='update'),
    path('<int:assignment_id>/delete/', AssignmentDeleteView.as_view(), name='delete'),
]
