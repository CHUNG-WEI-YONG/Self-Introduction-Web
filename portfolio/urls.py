from django.urls import path
from . import views

app_name='portfolio'
urlpatterns=[
    path('projects/', views.project_list_view, name='project_list'),
    path('projects/create/', views.project_create_view, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_update_view, name='project_update'),
    path('projects/<int:pk>/delete/', views.project_delete_view, name='project_delete'),

    # Technologies
    path('tech/', views.tech_stack_view, name='tech_stack'),
    path('tech/create/', views.tech_create_view, name='tech_create'),
    path('tech/<int:pk>/edit/', views.tech_update_view, name='tech_update'),    # 重点：确认这一行存在
    path('tech/<int:pk>/delete/', views.tech_delete_view, name='tech_delete'),

]