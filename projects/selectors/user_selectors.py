from projects.constants import SUPERVISOR
from projects.models.users import User
from django.db.models import Q


def get_users():
    return User.objects.all()


def get_user(username):
    return User.objects.get(username=username)


def get_user_by_id(id):
    return User.objects.get(pk=id)


def get_supervisors():
    return User.objects.filter(user_role=SUPERVISOR)


def get_other_supervisors(id):
    return User.objects.filter(~Q(pk=id), user_role='Supervisor')
