from django.urls import path

from . import views
from .home_view import home
from .admin_views import (admin_home, admin_projects, admin_profiles, 
                          student_projects_api, student_project_details, public_student_projects)
from .student_views import student_home, student_projects, delete_project, record_project_view, toggle_project_like, edit_project, remove_from_recent_uploads
from .notification_views import student_project_detail, toggle_follow, notifications, send_hire_notification
from .views import student_profile_view, request_follow, handle_follow_request

urlpatterns = [
    # Student profile URLs
    path('student/<int:student_id>/profile/', student_profile_view, name='student_profile'),
    path('student/<int:student_id>/request-follow/', request_follow, name='request_follow'),
    path('student/follow-request/<int:follow_id>/', handle_follow_request, name='handle_follow_request'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-student/', views.add_student, name='add_student'),
    path('developers/', public_student_projects, name='public_student_projects'),
    path('home/', home, name='home'),
    path('admin-home/', admin_home, name='admin_home'),
    path('admin-projects/', admin_projects, name='admin_projects'),
    path('admin-profiles/', admin_profiles, name='admin_profiles'),
    path('student-projects/<int:student_id>/', student_projects_api, name='student_projects_api'),
    path('student/<int:student_id>/projects/', student_project_details, name='student_project_details'),
    path('student-home/', student_home, name='student_home'),
    path('project/<int:project_id>/like/', toggle_project_like, name='toggle_project_like'),
    path('project/<int:project_id>/delete/', delete_project, name='delete_project'),
    path('project/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('project/<int:project_id>/remove-from-recent/', remove_from_recent_uploads, name='remove_from_recent_uploads'),
    path('project/<int:project_id>/details/', student_project_detail, name='student_project_detail'),
    path('project/<int:project_id>/hire/', send_hire_notification, name='send_hire_notification'),
    path('student/<int:student_id>/follow/', toggle_follow, name='toggle_follow'),
    path('notifications/', notifications, name='notifications'),
    path('projects/', student_projects, name='student_projects'),
        path('record-project-view/', record_project_view, name='record_project_view'),
    path('delete-project/<int:project_id>/', delete_project, name='delete_project'),
    path('', views.login_view, name='root'),
]
