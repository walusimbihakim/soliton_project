from projects.models.client_activity_rates import ClientActivityRate


def get_client_activity_rate(client, activity):
    return ClientActivityRate.objects.get(client, activity)