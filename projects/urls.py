# projects/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('search/', views.search, name='search'),

    path('api/projects/', views.ProjectList.as_view(), name='project_list_api'),
    path('api/projects/<int:pk>/', views.ProjectDetail.as_view(), name='project_detail_api'),

]

