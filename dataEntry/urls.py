
from django.urls import path
from . import views

urlpatterns = [
    path('',views.importData, name='import_data' )
]