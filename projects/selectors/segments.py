from projects.models import Segment


def get_all_segments():
    return Segment.objects.all()


def get_segment(id):
    return Segment.objects.get(pk=id)
