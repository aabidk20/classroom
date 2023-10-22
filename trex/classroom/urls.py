from django.urls import path, include
from .views import (
    ClassroomListView,
    ClassroomCreateView
)

app_name = "classroom"

urlpatterns = [
    path('', ClassroomListView.as_view(), name='list'),
    path('create/', ClassroomCreateView.as_view(), name='create'),
]