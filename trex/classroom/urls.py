from django.urls import path, include
from .views import (
    ClassroomListView,
    ClassroomCreateView,
    ClassroomDetailView,
    ClassroomUpdateView,
    ClassroomDeleteView
)

from trex.enrollment.views import (
    EnrollmentCreateView,
)

app_name = "classroom"

urlpatterns = [
    path('', ClassroomListView.as_view(), name='list'),
    path('create/', ClassroomCreateView.as_view(), name='create'),
    path('<int:classroom_id>/', ClassroomDetailView.as_view(), name='detail'),
    path('<int:classroom_id>/update/', ClassroomUpdateView.as_view(), name='update'),
    path('<int:classroom_id>/delete/', ClassroomDeleteView.as_view(), name='delete'),
    path('enroll/', EnrollmentCreateView.as_view(), name='enroll'),
]
