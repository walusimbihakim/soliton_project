from projects.models.materials import Material

def get_material(material_id):
    return Material.objects.get(pk=material_id)