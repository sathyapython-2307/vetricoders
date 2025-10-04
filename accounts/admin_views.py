from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from accounts.models import StudentProfile, Project
from django.utils.timesince import timesince

def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

@admin_required
def admin_home(request):
    candidates = StudentProfile.objects.count()
    total_projects = Project.objects.count()
    return render(request, 'accounts/admin_home.html', {
        'candidates': candidates,
        'total_projects': total_projects,
    })

@admin_required
def admin_projects(request):
    # Get all projects ordered by most recent first
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'accounts/admin_projects.html', {
        'projects': projects
    })

@admin_required
def admin_profiles(request):
    students = StudentProfile.objects.all().order_by('student_name')
    return render(request, 'accounts/admin_profiles.html', {
        'students': students
    })

@admin_required
def student_projects_api(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    projects = student.projects.all().order_by('-created_at')
    
    projects_data = [{
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'project_link': project.project_link,
        'output_link': project.output_link,
        'screenshot': project.screenshot.url if project.screenshot else None,
        'created_at_display': timesince(project.created_at)
    } for project in projects]
    
    return JsonResponse({'projects': projects_data})

@admin_required
def student_project_details(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    # For admin, show all projects (both public and private)
    projects = student.projects.all().order_by('-created_at')
    return render(request, 'accounts/student_project_details.html', {
        'student': student,
        'projects': projects,
        'is_admin': True
    })

def public_student_projects(request):
    students = StudentProfile.objects.all().order_by('student_name')
    for student in students:
        student.public_projects = student.projects.filter(visibility='Public').order_by('-created_at')
    return render(request, 'accounts/public_student_projects.html', {
        'students': students
    })
