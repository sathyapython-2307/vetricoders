from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Project, StudentProfile, StudentFollow, Notification
from django.utils import timezone

@login_required
def student_project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    is_following = False
    if request.user.is_authenticated:
        is_following = StudentFollow.objects.filter(
            follower=request.user,
            following=project.student
        ).exists()
    return render(request, 'accounts/student_project_details.html', {
        'project': project,
        'is_following': is_following
    })

@login_required
def toggle_follow(request, student_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    student = get_object_or_404(StudentProfile, id=student_id)
    
    # Don't allow self-following
    if student.user == request.user:
        return JsonResponse({'success': False, 'message': 'Cannot follow yourself'})
    
    follow, created = StudentFollow.objects.get_or_create(
        follower=request.user,
        following=student,
        defaults={'created_at': timezone.now()}
    )
    
    if not created:
        # User already follows, so unfollow
        follow.delete()
        following = False
    else:
        following = True
        # Create notification for new follower
        Notification.objects.create(
            recipient=student,
            sender=request.user,
            notification_type='follow'
        )
    
    return JsonResponse({
        'success': True,
        'following': following
    })

@login_required
def notifications(request):
    notifications = Notification.objects.filter(
        recipient=request.user.student_profile
    ).select_related('sender', 'project').order_by('-created_at')
    
    # Mark notifications as read
    notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'accounts/notifications.html', {
        'notifications': notifications
    })