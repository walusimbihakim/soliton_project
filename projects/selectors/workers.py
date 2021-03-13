from projects.models import Worker


def get_all_workers():
    return Worker.objects.all()


def get_all_workers_registered_by(user):
    return Worker.objects.filter(registered_by_user=user)


def get_worker(id):
    return Worker.objects.get(pk=id)
