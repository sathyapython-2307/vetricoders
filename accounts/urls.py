from django.urls import path

from . import views
from .home_view import home
from .admin_views import (admin_home, admin_projects, admin_profiles, 
                          student_projects_api, student_project_details, public_student_projects)
from .student_views import student_home, student_projects, delete_project

urlpatterns = [
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
    path('projects/', student_projects, name='student_projects'),
    path('delete-project/<int:project_id>/', delete_project, name='delete_project'),
    path('', views.login_view, name='root'),
]
