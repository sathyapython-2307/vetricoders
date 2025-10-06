from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_name = models.CharField(max_length=150)
    student_contact = models.CharField(max_length=30)
    student_email = models.EmailField()
    student_address = models.TextField()
    course_joined_date = models.DateField()
    course_details = models.TextField()
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.student_name

class Project(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    allow_downloads = models.BooleanField(default=False)
    category = models.CharField(default='Other', max_length=100)
    output_link = models.URLField(blank=True)
    project_link = models.URLField(blank=True)
    tags = models.CharField(blank=True, max_length=200)
    visibility = models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Public', max_length=20)
    screenshot = models.ImageField(upload_to='project_screenshots/', null=True, blank=True)

    def __str__(self):
        return self.title

    def view_count(self):
        return self.views.count()
        
    def like_count(self):
        return self.likes.count()
        
    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

class ProjectView(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')

class ProjectLike(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')

class StudentFollow(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]
    
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(StudentProfile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.student_name} ({self.status})"
        
    def accept(self):
        self.status = 'accepted'
        self.save()
        
    def reject(self):
        self.status = 'rejected'
        self.save()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Project Like'),
        ('follow', 'New Follow Request'),
        ('follow_accepted', 'Follow Request Accepted'),
    )

    recipient = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.notification_type == 'like':
            return f"{self.sender.username} liked your project {self.project.title}"
        return f"{self.sender.username} started following you"
