from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .i18n.bundle import bundles
from .i18n.i18n_openai import languages


def all_settings(request):
    if not settings.DEBUG:
        raise ImproperlyConfigured("ATTENTION! Production mode! Exposing full application settings prohibited.")

    settings_to_print = {}

    for name in dir(settings):
        if not name.startswith("_"):
            settings_to_print[name] = getattr(settings, name)

    return {
        'settings': settings_to_print
    }


def i18n_settings(request):
    lang = "eng"
    if request.GET:
        lang = request.GET.get('lang', "ikt")

    return {
        'bundles': bundles,
        'languages': languages,
        'curr_lang': lang
    }
