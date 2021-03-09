from projects.models.projects import *
from projects.models.survey import Survey


def get_projects():
    return Project.objects.all()


def get_project(project_id):
    return Project.objects.get(pk=project_id)

def get_project_types():
    return ProjectType.objects.all()


def get_project_type(project_type_id):
    return ProjectType.objects.get(pk=project_type_id)


def get_ducts():
    return DuctSystem.objects.all()

def get_surveys(project):
    surveys = Survey.objects.filter(project=project)
    return surveys


def get_survey(id):
    return Survey.objects.get(pk=id)
