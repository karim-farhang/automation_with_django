from django.apps import apps

def getModelsName():
    models = []
    for model in apps.get_models():
        if model.__name__ not in ['LogEntry','Permission','Group','User','ContentType','Session','Upload']:
            models.append(model.__name__)
    return models
