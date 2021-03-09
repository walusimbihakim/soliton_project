from projects.models import ExecutionScope
from django.db.models import Sum


def get_all_scopes():
    return ExecutionScope.objects.all()


def get_scopes(survey):
    return ExecutionScope.objects.filter(survey=survey)


def get_scope(id):
    return ExecutionScope.objects.get(pk=id)

def get_project_scopes(surveys):
    scopes = ExecutionScope.objects.filter(survey__in = surveys)
    
    scope_total = scopes.values('survey').annotate(scope_total=Sum('quantity'))

    return scope_total