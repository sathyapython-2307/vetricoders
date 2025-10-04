from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
@require_POST
def logout_view(request):
	logout(request)
	return redirect('/accounts/login/')
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import StudentProfile
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

@csrf_exempt
def add_student(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		student_name = request.POST.get('student_name')
		student_contact = request.POST.get('student_contact')
		student_email = request.POST.get('student_email')
		student_address = request.POST.get('student_address')
		course_joined_date = request.POST.get('course_joined_date')
		course_details = request.POST.get('course_details')
		student_image = request.FILES.get('student_image')
		if not username or not password:
			return JsonResponse({'success': False, 'error': 'Username and password required.'})
		if User.objects.filter(username=username).exists():
			return JsonResponse({'success': False, 'error': 'Username already exists.'})
		# Validate course_joined_date: must not be in the future
		try:
			joined_date = datetime.datetime.strptime(course_joined_date, '%Y-%m-%d').date()
			today = datetime.date.today()
			if joined_date > today:
				return JsonResponse({'success': False, 'error': 'Course joined date must not be in the future.'})
		except Exception:
			return JsonResponse({'success': False, 'error': 'Invalid course joined date.'})
		# Validate email uniqueness
		if StudentProfile.objects.filter(student_email=student_email).exists():
			return JsonResponse({'success': False, 'error': 'Email already exists.'})
		# Validate contact uniqueness
		if StudentProfile.objects.filter(student_contact=student_contact).exists():
			return JsonResponse({'success': False, 'error': 'Contact already exists.'})
		user = User.objects.create_user(username=username, password=password)
		user.is_superuser = False
		user.is_staff = False
		user.save()
		student_profile = StudentProfile(
			user=user,
			student_name=student_name,
			student_contact=student_contact,
			student_email=student_email,
			student_address=student_address,
			course_joined_date=course_joined_date,
			course_details=course_details
		)
		if student_image:
			student_profile.image = student_image
		student_profile.save()
		candidate_count = StudentProfile.objects.count()
		return JsonResponse({'success': True, 'candidates': candidate_count})
	return JsonResponse({'success': False, 'error': 'Invalid request.'})

def login_view(request):
	if request.method == 'POST':
		user_type = request.POST.get('user_type')
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request, username=email, password=password)
		if user is not None:
			if user_type == 'admin' and user.is_superuser:
				login(request, user)
				return redirect('/admin-home/')
			elif user_type == 'student' and not user.is_superuser:
				login(request, user)
				return redirect('/student-home/')
			else:
				messages.error(request, 'Invalid credentials for selected user type')
		else:
			messages.error(request, 'Invalid email or password')
	return render(request, 'accounts/login.html')
