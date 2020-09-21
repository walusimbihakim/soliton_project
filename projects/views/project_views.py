from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse

from projects.selectors.project_selectors import *
from projects.forms import *


# Create your views here.
def index_page(request):
    return render(request, "index.html")


def projects_page_view(request):
    form = ProjectForm()

    if request.method == "POST":
        ProjectForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()

            redirect('manage_projects')

    projects = get_projects()
    context = {
        'projects': projects,
        'form': form,
    }
    return render(request, "project/manage_projects.html", context)


def projects_settings_view(request):
    project_type_form = ProjectTypeForm()

    duct_form = DuctForm(request.POST, request.FILES)

    if request.method == "POST":
        project_type_form = ProjectTypeForm(request.POST, request.FILES)

        if project_type_form.is_valid():
            project_type_form.save()

        if duct_form.is_valid():
            duct_form.save()

    project_types = get_project_types()
    ducts = get_ducts()

    context = {
        "projects_settings_view": "active",
        "project_types": project_types,
        "duct_form": duct_form,
        "project_type_form": project_type_form,
        "ducts": ducts,
    }
    return render(request, "project/project_settings.html", context)


def project_details_view(request, project_id):
    project = get_project(project_id)

    context = {
        "project": project,
    }
    return render(request, "project/project_details.html", context)
