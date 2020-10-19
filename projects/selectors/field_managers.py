from projects.models import FieldManager


def get_all_field_managers():
    return FieldManager.objects.all()


def get_field_manager(id):
    return FieldManager.objects.get(pk=id)
