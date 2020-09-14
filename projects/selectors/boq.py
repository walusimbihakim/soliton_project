from projects.models.boqs import BOQ


def get_boq(id):
    return BOQ.objects.get(pk=id)
