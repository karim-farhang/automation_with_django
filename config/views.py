from django.shortcuts import render
from django.http import HttpResponse
import time
from dataEntry.celery_task import celery_test_task

def homeView(request):
    return render(request, 'home.html')


def celery_test(request):
    celery_test_task.delay()
    return render(request,'celery_test.html')