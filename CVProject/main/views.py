from django.shortcuts import render
from django.http import Http404, HttpResponse
from django_xhtml2pdf.utils import generate_pdf
from .models import CVDoc, RequestLog
from .tasks import send_cv_to_email
from .i18n.bundle import bundles


def home_page(request):
    all_cvs: [str] = list_all_cvs()
    return render(request, template_name="index.html", context={"all_cvs": all_cvs})


def cv_page(request, cv_id):
    cv: CVDoc = get_cv(cv_id)
    context = {"cv": cv}

    # Send email if POST request is received
    if request.POST and request.POST['email']:
        email = request.POST['email']
        pdf_content = generate_pdf(template_name='cv_pdf.html', context=context).getvalue()
        send_cv_to_email.delay(pdf_content, cv.pdf_file_name, cv.full_name, email)
        context['email_sent_to'] = email

    return render(request, template_name="cv.html", context=context)


def log_page(request):
    logs = RequestLog.objects.all().order_by('-timestamp')[:10]
    return render(request, template_name="logs.html", context={"logs": logs})


def settings_page(request):
    return render(request, template_name="settings.html")


def cv_pdf(request, cv_id, file_name):
    cv: CVDoc = get_cv(cv_id)
    context = {
        "cv": cv,
        "bundles": bundles
    }
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf(template_name='cv_pdf.html', context=context, file_object=resp)
    return result


def list_all_cvs() -> [dict]:
    return [{
        "id": cv.id,
        "name": cv.full_name
    } for cv in
        CVDoc.objects.all().order_by("lastname")
    ]


def get_cv(cv_id) -> CVDoc:
    try:
        return CVDoc.objects.get(id=cv_id)
    except CVDoc.DoesNotExist:
        raise Http404(f"CV entry with id={cv_id} is not found")

