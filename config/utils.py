from django.apps import apps
from django.core.mail import EmailMessage
from django.conf import settings



def getModelsName():
    models = []
    for model in apps.get_models():
        if model.__name__ not in ['LogEntry','Permission','Group','User','ContentType','Session','Upload']:
            models.append(model.__name__)
    return models


def send_email(subject=None, message=None, from_email=None, to_email=None):
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    if to_email is None:
        to_email = [settings.DEFAULT_TO_EMAIL]
    elif isinstance(to_email, str):
        to_email = [to_email]
    
    if subject is None:
        subject = 'Send email by Celery in Django'
    if message is None:
        message = 'This is the default message sent by Celery'

    try:
        email = EmailMessage(subject, message, from_email, to=to_email)
        email.send()
        return f'Email sent successfully to: {", ".join(to_email)}'
    except Exception as e:
        return f"Error: {e}"