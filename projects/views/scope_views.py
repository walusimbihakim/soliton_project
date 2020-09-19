from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from projects.forms.execution_scope_form import ExecutionScopeForm
from projects.selectors.project_selectors import get_projects, get_project, get_survey
from projects.selectors.scopes import get_all_scopes, get_scopes, get_scope
from projects.selectors.survey_selectors import get_surveys


def manage_scopes(request):
    projects = get_projects()
    context = {
        'projects': projects,
    }
    return render(request, "scope/manage_scopes.html", context)


def manage_project_scopes(request, id):
    project = get_project(id)
    surveys = get_surveys(project)
    context = {
        'surveys': surveys,
    }
    return render(request, "scope/manage_project_scopes.html", context)


def manage_survey_scopes(request, id):
    survey = get_survey(id)
    scopes = get_scopes(survey=survey)
    form = ExecutionScopeForm()

    if request.method == "POST":
        form = ExecutionScopeForm(request.POST, request.FILES)
        if form.is_valid():
            scope = form.save(commit=False)
            scope.survey = survey
            scope.save()
            messages.success(request, "Successfully added a scope")
        else:
            messages.error(request, "Integrity problems while saving scope")
        return HttpResponseRedirect(reverse(manage_survey_scopes, args=[survey.id]))
    context = {
        "manage_scopes": "active",
        "scopes": scopes,
        'form': form,
    }
    return render(request, "scope/manage_survey_scopes.html", context)


def delete_scope(request, id):
    scope = get_scope(id)
    survey = scope.survey
    scope.delete()
    messages.success(request, "Successfully deleted a scope")
    return HttpResponseRedirect(reverse(manage_survey_scopes, args=[survey.id]))


def edit_scope(request, id):
    scope = get_scope(id)
    survey = scope.survey
    form = ExecutionScopeForm(instance=scope)
    if request.method == "POST":
        form = ExecutionScopeForm(request.POST, request.FILES, instance=scope)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited a scope")
        else:
            messages.error(request, "Integrity problems while saving scope")
        return HttpResponseRedirect(reverse(manage_survey_scopes, args=[survey.id]))
    context = {
        "form": form,
    }
    return render(request, "scope/edit_scope.html", context)
