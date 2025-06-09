from django.urls import path
from django.views.generic import RedirectView
from . import views_api


urlpatterns = [
    path('',  RedirectView.as_view(url='cv')),
    path('add/', views_api.create_cv_doc),
    path('cv/', views_api.get_cv_list),
    path('cv/<int:cv_id>', views_api.CVDocGetUpdateDeleteView.as_view()),

]
