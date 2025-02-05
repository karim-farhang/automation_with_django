from config.celery import app
import time
from django.core.management import call_command


@app.task
def celery_test_task():
    time.sleep(10)
    return 'Celery Task test example'


@app.task
def celery_import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    return 'Data imported successfully'

