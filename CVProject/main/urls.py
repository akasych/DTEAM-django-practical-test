from django.urls import path
from .views import home_page, log_page, settings_page, cv_page, cv_pdf


urlpatterns = [
    path('',  home_page, name='home'),
    path('logs/',  log_page, name='logs'),
    path('settings/',  settings_page, name='settings'),
    path('cv/<int:cv_id>/',  cv_page, name='cv'),
    path('cv-pdf/<int:cv_id>/<str:file_name>', cv_pdf, name='cv-pdf'),
]
