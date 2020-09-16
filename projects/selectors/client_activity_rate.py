from clients.models import Client
from projects.models import Activity
from projects.models.client_activity_rates import ClientActivityRate


def get_client_activity_rate(client: Client, activity: Activity) -> int:
    try:
        client_activity_rate = ClientActivityRate.objects.get(client=client, activity=activity)
    except ClientActivityRate.DoesNotExist:
        return 0
    return client_activity_rate.rate


def get_client_activity_currency(client: Client, activity: Activity) -> int:
    try:
        client_activity_rate = ClientActivityRate.objects.get(client=client, activity=activity)
    except ClientActivityRate.DoesNotExist:
        return "UGX"
    return client_activity_rate.currency
