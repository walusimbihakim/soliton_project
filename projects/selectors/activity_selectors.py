from projects.models.activity_list import Activity

def get_activities():
    return Activity.objects.all()

def get_activity(id):
    return Activity.objects.get(pk=id)