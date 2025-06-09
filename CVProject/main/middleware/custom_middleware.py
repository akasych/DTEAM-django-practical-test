from django.utils.deprecation import MiddlewareMixin
from ..models import RequestLog


class RequestLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request._method = request.method
        request._url = request.path
        request._remote_host = request.META.get('REMOTE_HOST')

    def process_response(self, request, response):
        method = getattr(request, '_method', '')
        url = getattr(request, '_url', '')
        remote_host = getattr(request, '_remote_host', '')
        response_status = response.status_code

        RequestLog.objects.create(
            method=method,
            url=url,
            remote_ip=remote_host,
            response_status=response_status,
        )
        return response
