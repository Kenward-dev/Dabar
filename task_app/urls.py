"""
This module contains URL routing for the Taskly API, including user registration, login, and task management endpoints.
"""

from django.urls import path
from .views import (
    RegisterView, 
    EmailLoginView, 
    TaskListCreateView, 
    TaskDetailView,
    TaskUpdateStatusView,
    TaskCompletedListView,
    TaskPendingListView,
    toggle_task_status,
    task_stats
)

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', EmailLoginView.as_view(), name='email_login'),
    
    # Main task CRUD operations
    path('tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    
    # Task status operations
    path('tasks/<int:pk>/status/', TaskUpdateStatusView.as_view(), name='task-update-status'),
    path('tasks/<int:pk>/toggle/', toggle_task_status, name='task-toggle-status'),
    
    # Filtered task lists
    path('tasks/completed/', TaskCompletedListView.as_view(), name='task-completed-list'),
    path('tasks/pending/', TaskPendingListView.as_view(), name='task-pending-list'),
    
    # Task statistics
    path('tasks/stats/', task_stats, name='task-stats'),
]