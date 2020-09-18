from projects.models import ExecutionScope


def get_all_scopes():
    return ExecutionScope.objects.all()