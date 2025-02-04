from django.shortcuts import render, redirect
from django.core.management import call_command
from config.utils import getModelsName
from uploads.models import Upload
from config.settings import BASE_DIR
from .celery_task import celery_import_data_task, celery_test_task


def importData(request):

    models = getModelsName()
    context = {'models': models, 'error': ''}

    if request.method == 'POST':

        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        upload = Upload.objects.create(csv_file=file_path, model_name=model_name)

        relative_path = str(upload.csv_file.url)
        absultly_path = str(BASE_DIR)

        path = absultly_path+relative_path

        celery_import_data_task.delay(file_path=path, model_name=model_name)
        
        messae = 'You data begin uploading when completed you find a notifcation'
        context['error'] = f': {messae}'

        return render(request, 'dataentery/importdata.html', context)

    return render(request, 'dataentery/importdata.html', context)
