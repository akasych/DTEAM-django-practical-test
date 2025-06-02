from django.urls import path
from .views import home_page, cv_page


urlpatterns = [
    path('',  home_page),
    path('cv/<int:cv_id>',  cv_page),
]
