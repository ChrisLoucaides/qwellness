from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import render, redirect
from .forms import SignupForm
from django.utils import timezone

from .models import Student, Advisor


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Hash the password before saving the user
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.advisor = form.cleaned_data['advisor']
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.last_login_time = timezone.now()
            user.save()
            response = HttpResponseRedirect('http://localhost:5173/')
            response.set_cookie('user_id', str(user.id))
            return response
        else:
            print("Authentication failed for user:", username)
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('/login')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def get_user_info(request):
    # noinspection PyUnresolvedReferences
    user_info = {
        "id": request.user.id,
        "username": request.user.username,
        "first_name": request.user.first_name,
        "role": request.user.role,
        "advisor": getattr(request.user.advisor, 'username', None),
        "last_login_time": request.user.last_login_time
    }
    return JsonResponse(user_info)


@login_required()
def filter_advisors_students(request):
    if request.method == 'GET':
        advisor_username = request.GET.get('username')
        print(advisor_username)

        try:
            advisor = Advisor.objects.get(username=advisor_username)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Advisor not found'}, status=404)

        students = Student.objects.filter(advisor=advisor)

        serialized_students = []
        for student in students:
            serialized_student = {
                'username': student.username,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'last_login_time': student.last_login_time,
                'email': student.email
            }
            serialized_students.append(serialized_student)

        return JsonResponse({'students': serialized_students})

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
