from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


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

