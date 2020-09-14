from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from projects.models.boqs import BOQ
from projects.selectors.boq import get_boq
from projects.selectors.project_selectors import get_projects, get_project, get_surveys, get_survey


def manage_boqs(request):
    projects = get_projects()
    context = {
        'projects': projects,
    }
    return render(request, "boq/manage_boqs.html", context)


def manage_project_boqs(request, id):
    project = get_project(id)
    surveys = get_surveys(project)
    context = {
        'surveys': surveys,
    }
    return render(request, "boq/manage_project_boqs.html", context)


def manage_boq_items(request, id):
    boq = get_boq(id)
    context = {
        'surveys': "",
    }
    return render(request, "boq/manage_boq_items.html", context)


def create_boq(request, survey_id):
    survey = get_survey(survey_id)
    try:
        boq = BOQ.objects.create(
            survey=survey
        )
    except Exception:
        boq = survey.boq

    return HttpResponseRedirect(reverse(manage_boq_items, args=[boq.id]))
