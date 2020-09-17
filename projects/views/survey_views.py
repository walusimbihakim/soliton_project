from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse

from projects.forms.survey_form import *
from projects.selectors.survey_selectors import *
from projects.selectors.project_selectors import *


def survey_page_view(request, id):
    survey_form = SurveyForm(initial={'project':get_project(id)})

    if request.method=="POST":
        survey_form = SurveyForm(request.POST, request.FILES)
        
        if survey_form.is_valid():
            survey_form.save()

            messages.success(request, "Survey Saved Successfully")
    
    surveys = get_surveys()

    context = {
        "surveys": surveys,
        "survey_form": survey_form,
        "project": get_project(id)
    }

    return render(request, "manage_surveys.html", context)

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
    return render(request, "edit_survey.html", context)

def delete_survey(request, survey_id):
    survey = get_survey(survey_id)

    survey.delete()
    
    messages.success(request, "Successfully Deleted activity")
    return HttpResponseRedirect(reverse(survey_page_view, args=[survey.project.id]))