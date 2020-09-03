from projects.models.sites import *

def get_sites(project_id):
    return Site.objects.filter(project=project_id)

def get_site(site_id):
    return Site.objects.get(pk=site_id)
