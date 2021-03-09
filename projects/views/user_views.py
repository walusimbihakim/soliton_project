from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from projects.decorators.auth_decorators import super_admin_required
from projects.forms.user_forms import UserForm
from projects.selectors.user_selectors import get_users, get_user_by_id
from django.shortcuts import render


@super_admin_required
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
        "manage_users": "active"
    }

    return render(request, "users/manage_user.html", context)


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

    return render(request, "users/edit_user.html", context)


def delete_user_view(request, id):
    user = get_user_by_id(id)

    user.delete()
    messages.success(request, 'User Deleted Successfully')

    return HttpResponseRedirect(reverse(manage_user_view))
