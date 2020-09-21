from projects.models.pip import PIP, Predecessor

def get_pips(scope_id):
    pips = PIP.objects.filter(scope=scope_id)

    return pips
    
def get_pip(pip_id):
    pip = PIP.objects.get(pk=pip_id)

    return pip