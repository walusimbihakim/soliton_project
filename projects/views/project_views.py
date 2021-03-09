from django.shortcuts import render, redirect
from projects.decorators.auth_decorators import project_manager_required
from projects.selectors.project_selectors import get_project, get_projects, get_project_types, get_ducts
from projects.selectors.survey_selectors import get_surveys
from projects.selectors.scopes import get_project_scopes
from projects.selectors.boq import get_project_material_boqs, get_project_service_boqs
from projects.forms.project_forms import ProjectForm, ProjectTypeForm, DuctForm


def dashboard_page(request):
    return render(request, "index.html")


@project_manager_required
def projects_page_view(request):
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            redirect('manage_projects')

    projects = get_projects()
    context = {
        'projects': projects,
        'form': form,
    }
    return render(request, "project/manage_projects.html", context)


@project_manager_required
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


@project_manager_required
def project_details_view(request, project_id):
    project = get_project(project_id)

    surveys = get_surveys(project)

    material_boqs = get_project_material_boqs(surveys)
    service_boqs = get_project_service_boqs(surveys)
    project_scopes = get_project_scopes(surveys)

    context = {
        "project": project,
        "surveys": surveys,
        "material_boqs": material_boqs,
        "service_boqs": service_boqs,
        "project_scopes": project_scopes,
    }
    return render(request, "project/project_details.html", context)
