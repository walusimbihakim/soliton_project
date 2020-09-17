from projects.models.survey import *

def get_surveys():
    return Survey.objects.all()

def get_survey(survey_id):
    return Survey.objects.get(pk=survey_id)