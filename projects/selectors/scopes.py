from projects.models import ExecutionScope


def get_all_scopes():
    return ExecutionScope.objects.all()


def get_scopes(survey):
    return ExecutionScope.objects.filter(survey=survey)


def get_scope(id):
    return ExecutionScope.objects.get(pk=id)
