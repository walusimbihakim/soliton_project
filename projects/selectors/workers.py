from projects.models import Worker


def get_all_workers():
    return Worker.objects.all()


def get_worker(id):
    return Worker.objects.get(pk=id)
