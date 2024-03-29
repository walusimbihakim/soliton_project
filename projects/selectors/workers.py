from django.db.models import Q, Count

from projects.models import Worker, GroupWorker


def get_all_workers():
    return Worker.objects.all()


def get_all_workers_registered_by(user):
    return Worker.objects.filter(Q(registered_by_user=user) | Q(assigned_to=user))


def get_all_worker_groups_supervised_by(user):
    return GroupWorker.objects.filter(supervisor=user)


def get_worker(id):
    return Worker.objects.get(pk=id)


def get_worker_phone_number(phone_number):
    return Worker.objects.get(mobile_money_number=phone_number)


def get_group_worker(id):
    return GroupWorker.objects.get(pk=id)


def get_workers_per_gender():
    return Worker.objects.values("gender").annotate(total = Count('gender')).order_by()

    