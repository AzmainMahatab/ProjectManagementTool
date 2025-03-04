# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('projects/<int:project_id>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:task_id>/toggle/', views.task_toggle_complete, name='task_toggle_complete'),
]