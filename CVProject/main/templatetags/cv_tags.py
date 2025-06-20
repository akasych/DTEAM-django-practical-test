from django import template
from ..models import CVDoc, RequestLog

register = template.Library()


@register.simple_tag(name='cv_list')
def get_cvs() -> [dict]:
    return list_all_cvs()


@register.inclusion_tag('logs_list.html')
def show_logs():
    logs = RequestLog.objects.all().order_by('-timestamp')[:10]
    return {"logs": logs}


def list_all_cvs() -> [dict]:
    return [{
        "id": cv.id,
        "name": cv.full_name
    } for cv in
        CVDoc.objects.all().order_by("lastname")
    ]
