from projects.models.boqs import BOQ, MaterialBOQItem, ServiceBOQItem


def get_boq(id):
    return BOQ.objects.get(pk=id)


def get_materialboqitems(boq):
    return MaterialBOQItem.objects.filter(boq=boq)


def get_serviceboqitems(boq):
    return ServiceBOQItem.objects.filter(boq=boq)
