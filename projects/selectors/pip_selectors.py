from projects.models.pip import PIP

def get_pips(scope_id):
    pips = PIP.objects.filter(scope=scope_id)

    return pips
    
def get_pip(pip_id):
    pip = PIP.objects.get(pk=pip_id)

    return pip

def get_project_pips(surveys):
    boqs = BOQ.objects.filter(survey__in=surveys)
    material_boqs = MaterialBOQItem.objects.filter(boq__in = boqs)
    material_boqs_totals = material_boqs.values('material').annotate(material_total=Sum('quantity'))

    return material_boqs_totals
