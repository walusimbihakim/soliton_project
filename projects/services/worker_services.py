from projects.models.workers import WorkerAssignment


def create_worker_transfer(worker, new_assigned_supervisor_user):
    worker_assignment = WorkerAssignment.objects.create(
        worker=worker,
        from_supervisor=worker.assigned_to,
        to_supervisor=new_assigned_supervisor_user
    )
    worker.assigned_to = new_assigned_supervisor_user
    return worker_assignment
