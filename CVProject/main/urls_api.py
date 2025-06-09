from django.urls import path
from . import views_api


urlpatterns = [
    path('',  views_api.redirect_to_list),
    path('list',  views_api.CVDocListView.as_view()),

]
