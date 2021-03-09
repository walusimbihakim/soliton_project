from projects.models import Team, PIPTeam


def get_all_teams():
    return Team.objects.all()


def get_team(id):
    return Team.objects.get(pk=id)


def get_all_pip_teams():
    return PIPTeam.objects.all()


def get_pip_team(id):
    return PIPTeam.objects.get(pk=id)
