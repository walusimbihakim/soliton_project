from .models import User


def get_users():
    return User.objects.all()


def get_user(username):
    return User.objects.get(username=username)


def get_user_by_id(id):
    return User.objects.get(pk=id)
