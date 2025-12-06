from time import sleep
from celery import shared_task

@shared_task
def notify_customers(message):
    print(f'Sending notification to 10k customers: {message}')
    sleep(5)
    print('10k customers notified successfully')