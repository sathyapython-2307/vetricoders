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
