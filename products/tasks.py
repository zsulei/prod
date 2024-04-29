from celery import  shared_task
from django.http import HttpResponse

@shared_task
def parse_task():
    from .utils import start_func
    request = None
    response = start_func(request)
    return str(response.content)