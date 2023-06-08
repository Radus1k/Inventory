from celery import shared_task

@shared_task
def testing_task():
    print("********************************\n\n\n\ TEST OK! ********************************")