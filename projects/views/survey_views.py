from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib import messages

from projects.forms.survey_form import *
from projects.selectors.survey_selectors import get_surveys
from projects.selectors.project_selectors import *


def survey_page_view(request, id):
    survey_form = SurveyForm(initial={'project': get_project(id)})

    if request.method == "POST":
        survey_form = SurveyForm(request.POST, request.FILES)

        if survey_form.is_valid():
            survey_form.save()

            messages.success(request, "Survey Saved Successfully")

    project = get_project(id)
    surveys = get_surveys(project)

    context = {
        "surveys": surveys,
        "survey_form": survey_form,
        "project": get_project(id)
    }

    return render(request, "survey/manage_surveys.html", context)


def edit_survey(request, id, survey_id):
    survey = get_survey(survey_id)

    survey_form = SurveyForm(instance=survey)

    if request.method == "POST":
        survey_form = SurveyForm(request.POST, instance=survey)

        if survey_form.is_valid():
            survey_form.save()

            messages.success(request, "Changes saved Successfully")
            return HttpResponseRedirect(reverse(survey_page_view, args=[id]))

    context = {
        "survey": get_survey(survey_id),
        "survey_form": survey_form,
        "project": get_project(id)
    }
    return render(request, "survey/edit_survey.html", context)


def delete_survey(request, survey_id):
    survey = get_survey(survey_id)

    survey.delete()

    messages.success(request, "Successfully Deleted activity")
    return HttpResponseRedirect(reverse(survey_page_view, args=[survey.project.id]))
