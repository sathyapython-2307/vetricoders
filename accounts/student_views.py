from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Project

@login_required
def student_projects(request):
    projects = Project.objects.filter(student=request.user.student_profile).order_by('-created_at')
    return render(request, 'accounts/projects.html', {'projects': projects})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, student=request.user.student_profile)
    if request.method == 'POST':
        project.delete()
        return redirect('student_projects')
    return redirect('student_projects')

@login_required
def student_home(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Handle AJAX project creation
            project = Project.objects.create(
                student=request.user.student_profile,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                category=request.POST.get('category'),
                tags=request.POST.get('tags'),
                visibility=request.POST.get('visibility'),
                allow_downloads=request.POST.get('allow_downloads') == 'on',
                output_link=request.POST.get('output_link', ''),
                project_link=request.POST.get('project_link', '')
            )
            
            # Handle screenshot if provided
            if 'screenshot' in request.FILES:
                project.screenshot = request.FILES['screenshot']
                project.save()
            
            return JsonResponse({'success': True, 'message': 'Project created successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    # Pass user_projects for Recent Uploads
    user_projects = Project.objects.filter(student=request.user.student_profile).order_by('-created_at')[:6]
    return render(request, 'accounts/student_home.html', {'user_projects': user_projects})
