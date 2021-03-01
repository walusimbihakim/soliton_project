from authentication.forms import UserForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages

from .selectors import get_user, get_user_by_id, get_users
from .decorators import login_required


def user_login_view(request):

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = get_user(username=username)

        if user.password == password:
            # request.session['username'] = user.username
            return HttpResponseRedirect(reverse('index_page'))
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "auth/login.html")
    else:
        return render(request, "auth/login.html")


@login_required
def manage_user_view(request):
    user_form = UserForm()

    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'User registered Successfully')
        else:
            messages.error(
                request, "Registration Failed, CHeck your input and try again")

        return HttpResponseRedirect(reverse(manage_user_view))

    users = get_users()

    context = {
        "users": users,
        "user_form": user_form,
    }

    return render(request, "auth/manage_user.html", context)


@login_required
def edit_user_view(request, id):
    user = get_user_by_id(id)

    user_form = UserForm(instance=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES, instance=user)

        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'User info changed Successfully')
        else:
            messages.error(request, 'User update failed')

        return HttpResponseRedirect(reverse(manage_user_view))

    context = {
        "user_form": user_form,
        "user": user
    }

    return render(request, "auth/edit_user.html", context)


def delete_user_view(request, id):
    user = get_user_by_id(id)

    user.delete()
    messages.success(request, 'User Deleted Successfully')

    return HttpResponseRedirect(reverse(manage_user_view))
