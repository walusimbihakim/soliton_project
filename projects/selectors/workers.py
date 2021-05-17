from django.db.models import Q

from projects.models import Worker



def get_all_workers():
    return Worker.objects.all()


def get_all_workers_registered_by(user):
    return Worker.objects.filter(Q(registered_by_user=user)|Q(assigned_to=user))


def get_worker(id):
    return Worker.objects.get(pk=id)

