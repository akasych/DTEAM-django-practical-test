from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('',  home_page, name='home'),
    path('logs/',  log_page, name='logs'),
    path('settings/',  settings_page, name='settings'),
    path('cv/<int:cv_id>/',  cv_page, name='cv'),
    path('cv-pdf/<int:cv_id>/<str:file_name>', cv_pdf, name='cv-pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
