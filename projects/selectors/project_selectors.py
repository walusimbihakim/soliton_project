from projects.models.projects import *

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
