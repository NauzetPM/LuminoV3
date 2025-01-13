from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm


def user_signup(request):
    if request.method == 'POST':
        if (form := SignupForm(request.POST)).is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Welcome to Lumino. Nice to see you!')
            return redirect('subjects:subjects_list')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', dict(form=form))


def user_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def user_login(request):
    FALLBACK_REDIRECT = 'subjects:subjects_list'

    if request.user.is_authenticated:
        return redirect(FALLBACK_REDIRECT)
    login_error = False
    next = request.GET.get('next')

    if request.method == 'POST':
        if (form := LoginForm(request.POST)).is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user := authenticate(request, username=username, password=password):
                login(request, user)
                messages.success(request, 'Welcome to Lumino. Nice to see you!')
                return redirect(request.GET.get('next', FALLBACK_REDIRECT))
            else:
                login_error = True

    else:
        form = LoginForm()
    return render(
        request,
        'registration/login.html',
        dict(form=form, login_error=login_error, next=next),
    )
