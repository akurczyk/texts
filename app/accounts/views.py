from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.shortcuts import render, redirect

from .forms import UserForm, ProfileForm


def create(request):
    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            user_form.instance.profile.bio = profile_form.cleaned_data['bio']
            user_form.instance.profile.location = profile_form.cleaned_data['location']
            user_form.instance.profile.save()
            messages.success(request, 'Konto zostało utworzone! Teraz możesz się zalogować.')
            return redirect('login')
        else:
            messages.error(request, 'Konto nie zostało utworzone, z powodu błędów. Popraw je i spróbuj ponownie :-)')

    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/create.html', context)


@login_required
def edit(request):
    if request.method == 'POST' and request.POST['action'] == 'profile_change':
        user_form = UserForm(data=request.POST, instance=request.user)
        profile_form = ProfileForm(data=request.POST, instance=request.user.profile)
        password_form = SetPasswordForm(user=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Zmiany zostały zapisane!')
            return redirect('edit_user')
        else:
            messages.error(request, 'Zmiany nie zostały zapisane z powodu błędów. Popraw je i spróbuj ponownie :-)')

    elif request.method == 'POST' and request.POST['action'] == 'password_change':
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_form = SetPasswordForm(data=request.POST, user=request.user)

        if password_form.is_valid():
            password_form.save()
            messages.success(request, 'Zmiany zostały zapisane!')
            return redirect('edit_user')
        else:
            messages.error(request, 'Zmiany nie zostały zapisane z powodu błędów. Popraw je i spróbuj ponownie :-)')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_form = SetPasswordForm(user=request.user)

    context = {
        'user_form': user_form,
        'password_form': password_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/edit.html', context)
