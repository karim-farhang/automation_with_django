from config.celery import app
import time
from django.core.management import call_command
from config.utils import send_email

@app.task
def celery_test_task():
    time.sleep(5)
    y = send_email(
        subject="Hello!",
        message="This is a test email.",
        to_email=["midatechnical@gmail.com","karimfarhang2018@gmail.com", "atfarhadi313@gmail.com"]
    )
    return f'Email send successful Task completed {y}'


@app.task
def celery_import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    return 'Data imported successfully'
