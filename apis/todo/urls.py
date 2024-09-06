from django.urls import path
from . import views

urlpatterns = [
    path("task-list/", views.TaskListView.as_view(), name="task-list"),
    path("task-list/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
]
