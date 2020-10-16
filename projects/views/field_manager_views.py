from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from projects.forms.field_manager_form import FieldManagerForm
from projects.selectors.field_managers import get_all_field_managers, get_field_manager


def manage_field_managers(request):
    field_managers = get_all_field_managers()
    form = FieldManagerForm()
    if request.method == "POST":
        form = FieldManagerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added a field manager")
        else:
            messages.error(request, "Integrity problems while saving worker")
        return HttpResponseRedirect(reverse(manage_field_managers))
    context = {
        "wagebill": "active",
        "manage_field_managers": "active",
        "field_managers": field_managers,
        'form': form,
    }
    return render(request, "field_manager/manage_field_managers.html", context)


def edit_field_manager(request, id):
    field_manager = get_field_manager(id)
    form = FieldManagerForm(instance=field_manager)
    if request.method == "POST":
        form = FieldManagerForm(request.POST, request.FILES, instance=field_manager)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited a Field Manager")
        else:
            messages.error(request, "Integrity problems while saving worker")
        return HttpResponseRedirect(reverse(manage_field_managers))
    context = {
        "wagebill": "active",
        "manage_workers": "active",
        "form": form,
    }
    return render(request, "field_manager/edit_field_manager.html", context)


def delete_field_manager(request, id):
    field_manager = get_field_manager(id)
    field_manager.delete()
    messages.success(request, "Successfully deleted a field manager")
    return HttpResponseRedirect(reverse(manage_field_managers))
