from projects.models.survey import *

def get_surveys(project):
    surveys = Survey.objects.filter(project=project)
    return surveys


def get_survey(id):
    return Survey.objects.get(pk=id)