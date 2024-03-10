from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import render, redirect
from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Hash the password before saving the user
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html',
                  {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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
        "advisor": getattr(request.user.advisor, 'username', None)
    }
    return JsonResponse(user_info)
