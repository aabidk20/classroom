from django.urls import path, include

from .views import (
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)

app_name = "user"

urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("<int:id>/", UserDetailView.as_view(), name="detail"),
    path("create/", UserCreateView.as_view(), name="create"),
    path("<int:id>/update/", UserUpdateView.as_view(), name="update"),
    path("<int:id>/delete/", UserDeleteView.as_view(), name="delete"),
]
