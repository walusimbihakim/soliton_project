from projects.models.budget import Budget


def create_pip_budget(pip):
    try:
        budget = Budget.objects.create(
            pip=pip
        )
    except Exception:
        budget = pip.budget
    return budget
