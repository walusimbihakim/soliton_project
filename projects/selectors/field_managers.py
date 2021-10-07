from projects.models import FieldManager, User, WageSheet, Wage
from projects.models.users import FieldManagerAssignment


def get_all_field_managers():
    return FieldManager.objects.all()


def get_field_manager(id):
    return FieldManager.objects.get(pk=id)


def get_field_manager_from_worker(worker):
    try:
        supervisor = worker.assigned_to
        field_manager = supervisor.field_manager_assignment.field_manager_user
    except FieldManagerAssignment.DoesNotExist:
        field_manager = None
    return field_manager


def get_the_latest_wage_field_manager(worker):
    try:
        wage = Wage.objects.filter(worker=worker).order_by('-id')[0]
    except IndexError:
        return None
    return wage.wage_sheet.field_manager_user
