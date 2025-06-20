from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .i18n.bundle import bundles
from .i18n.i18n_openai import languages, translate_list


def all_settings(request):
    if not settings.DEBUG:
        print("ImproperlyConfigured: ATTENTION! Production mode! Exposing full application settings prohibited.")
        # raise ImproperlyConfigured("ATTENTION! Production mode! Exposing full application settings prohibited.")

    settings_to_print = {}

    for name in dir(settings):
        if not name.startswith("_"):
            settings_to_print[name] = getattr(settings, name)

    return {
        'settings': settings_to_print
    }


def i18n_settings(request):
    target_bundles = bundles
    # resolving target language from request
    target_lang_code = "eng"
    if request.GET:
        target_lang_code = request.GET.get('lang', "eng")

    # translate to target language if it's available and not default (eng)
    if not target_lang_code == "eng":
        target_language = [item['language'] for item in languages if item['code'] == target_lang_code][0]
        if target_language:
            bundle_keys = [key for key, value in bundles.items()]
            bundle_strings = [value for key, value in bundles.items()]
            translated_strings = translate_list(bundle_strings, target_language=target_language)
            if translated_strings:
                target_bundles = dict(zip(bundle_keys, translated_strings))

    return {
        'bundles': target_bundles,
        'languages': languages,
        'curr_lang': target_lang_code
    }
