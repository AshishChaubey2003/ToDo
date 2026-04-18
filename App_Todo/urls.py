from django.urls import path
from . import views

app_name = 'App_Todo'

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Tasks
    path('', views.task_list, name='task_list'),
    path('add/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('toggle/<int:pk>/', views.task_toggle_complete, name='task_toggle'),

    # Dashboard & Reports
    path('dashboard/', views.dashboard, name='dashboard'),
    path('weekly-report/', views.weekly_report, name='weekly_report'),

    # APIs
    path('check-consistency/', views.check_consistency, name='check_consistency'),
    path('daily-reminder/', views.daily_reminder, name='daily_reminder'),
    path('streak/', views.streak_api, name='streak'),
]