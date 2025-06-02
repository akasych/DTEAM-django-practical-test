from django.shortcuts import render
from django.http import Http404
from .models import CVDoc, Skill, Project

def home_page(request):
    all_cvs: [str] = list_all_cvs()
    return render(request, template_name="index.html", context={"all_cvs": all_cvs})


def cv_page(request, cv_id):
    cv: CVDoc = get_cv(cv_id)
    return render(request, template_name="cv.html", context={"cv": cv, "fullname": cv.get_full_name()})


def list_all_cvs() -> [dict]:
    return [{
        "id": cv.id,
        "name": cv.get_full_name()
    } for cv in
        CVDoc.objects.all().order_by("lastname")
    ]


def get_cv(cv_id) -> CVDoc:
    try:
        return CVDoc.objects.get(id=cv_id)
    except CVDoc.DoesNotExist:
        raise Http404(f"CV entry with id={cv_id} is not found")

