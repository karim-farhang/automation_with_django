from django.contrib import admin
from django.urls import path, include
from .views import homeView, celery_test
from django.conf.urls.static import static
from django.conf import settings
from users.views import registerUser, loginUser, logoutUser

from dataEntry.views import importData

urlpatterns = [
    path('admin/', admin.site.urls),

    # dashboard
    path('', homeView, name='home'),

    # user authentication
    path('register/', registerUser, name='register'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),


    path('import_data/', importData, name='import_data'),
    path('import_data/', include('dataEntry.urls')),


    path('celery_test/', celery_test, name='celery_test'),

    # Celery Test Route
    path('celery_test/', celery_test, name='celery_test'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
