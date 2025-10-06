from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Project, ProjectView, ProjectLike

@login_required
def student_projects(request):
    projects = Project.objects.filter(student=request.user.student_profile).order_by('-created_at')
    # Build list of project IDs for which to record views (not admin, not owner)
    record_view_ids = []
    if not request.user.is_superuser:
        for project in projects:
            if request.user != project.student.user:
                record_view_ids.append(project.id)
    return render(request, 'accounts/projects.html', {
        'projects': projects,
        'record_view_ids': record_view_ids
    })

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, student=request.user.student_profile)
    if request.method == 'POST':
        project.delete()
        return JsonResponse({'success': True, 'message': 'Project deleted successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def toggle_project_like(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        like, created = ProjectLike.objects.get_or_create(
            project=project,
            user=request.user,
            defaults={'created_at': timezone.now()}
        )
        
        if not created:
            # User already liked the project, so unlike it
            like.delete()
            liked = False
        else:
            liked = True
            
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likeCount': project.like_count()
        })
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

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

def view_project(request, project_id):
    project = Project.objects.get(id=project_id)
    user = request.user
    # Only count if not admin and not the owner
    if not user.is_superuser and user != project.student.user:
        ProjectView.objects.get_or_create(project=project, user=user)
    return render(request, 'accounts/project_detail.html', {'project': project})


@login_required
def record_project_view(request):
    print("\n=== Project View Request ===")
    print(f"Method: {request.method}")
    print(f"User: {request.user.username} (authenticated: {request.user.is_authenticated})")
    print(f"POST data: {request.POST}")
    print("Headers:")
    for key, value in request.headers.items():
        print(f"  {key}: {value}")
    
    if request.method == 'POST' and request.user.is_authenticated:
        project_id = request.POST.get('project_id')
        print(f"\nProcessing project_id: {project_id}")
        
        try:
            project = Project.objects.get(id=project_id)
            print(f"Found project: {project.title}")
            
            user = request.user
            print(f"User is superuser: {user.is_superuser}")
            print(f"Project owner: {project.student.user.username}")
            
            # Only create new view if not admin and not the owner
            if not user.is_superuser and user != project.student.user:
                view, created = ProjectView.objects.get_or_create(project=project, user=user)
                print(f"View record {'created' if created else 'already exists'}")
                if created:
                    print("New view recorded!")
                else:
                    print("User has already viewed this project")
            else:
                print("View not counted - user is admin or project owner")
            
            # Always return current count
            current_count = project.view_count()
            print(f"Current view count: {current_count}")
            
            response_data = {
                'success': True,
                'newCount': current_count,
                'projectId': project_id
            }
            print(f"Sending response: {response_data}")
            return JsonResponse(response_data)
            
        except Project.DoesNotExist:
            print(f"Error: Project {project_id} not found")
            return JsonResponse({'success': False, 'error': 'Project not found.'})
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    print("Invalid request - not POST or user not authenticated")
    return JsonResponse({'success': False, 'error': 'Invalid request.'})
