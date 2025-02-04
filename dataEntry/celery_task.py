from config.celery import app
import time
from django.core.management import call_command


@app.task
def celery_test_task():
    time.sleep(10)
    return 'Celery Task test example'


@app.task
def celery_import_data_task(file_path=None, model_name=None):
    if (file_path and model_name) is not None:
        try:
            call_command('importdata', file_path, model_name)
        except Exception as e:
            raise e
        return 'data imported successfuly'
    else:
        raise f'file path {file_path} or model name {model_name} is none'
    
