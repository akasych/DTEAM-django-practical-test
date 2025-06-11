from django.urls import path
from .views import home_page, log_page, settings_page, cv_page, cv_pdf


urlpatterns = [
    path('',  home_page),
    path('logs/',  log_page),
    path('settings/',  settings_page),
    path('cv/<int:cv_id>/',  cv_page),
    path('cv-pdf/<int:cv_id>/<str:file_name>',  cv_pdf),
]
