from django.shortcuts import render
from .models import CVDoc


def home_page(request):
    all_cvs: [str] = list_cv_names()
    return render(request, template_name="index.html", context={"all_cvs": all_cvs})


def list_cv_names() -> [str]:
    return [cv.get_full_name() for cv in CVDoc.objects.all()]
