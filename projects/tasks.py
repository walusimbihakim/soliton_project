from time import sleep

from celery import shared_task


@shared_task(bind=True)
def go_to_sleep(self, duration):
    sleep(duration)
    print("Non blocking task Done")
    return 'Done'
