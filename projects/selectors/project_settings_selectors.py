from projects.models import UnitOfMeasure

def get_measures():
    return UnitOfMeasure.objects.all()