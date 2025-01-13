from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from users.models import Profile

from .forms import EditProfileForm


@login_required
def user_edit(request):
    user = request.user
    profile = user.profile
    if user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            messages.success(request, 'User profile has been successfully saved.')
            form.save()
            return redirect('user_detail', user.username)
    form = EditProfileForm(instance=profile)
    return render(
        request,
        'user_edit.html',
        {'form': form, 'user': user, 'profile': profile},
    )


@login_required
def user_detail(request, username):
    user = get_user_model().objects.get(username=username)
    isteacher = Profile.is_teacher(user)
    if isteacher:
        roll = 'Teacher'
    else:
        roll = 'Student'
    return render(
        request,
        'user_info.html',
        {'user': user, 'roll': roll},
    )


@login_required
def leave(request):
    user = request.user
    if user.profile.role == Profile.Role.TEACHER:
        return HttpResponseForbidden()
    user.delete()
    messages.success(request, 'Good bye! Hope to see you soon.')
    return redirect('home')
