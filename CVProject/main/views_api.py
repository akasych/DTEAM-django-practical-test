from django.http import HttpResponseRedirect
from rest_framework import generics
from .serializers import CVDocSerializer
from .models import CVDoc


def redirect_to_list(request):
    return HttpResponseRedirect('/api/list')


class CVDocListView(generics.ListAPIView):
    queryset = CVDoc.objects.all().order_by("lastname")
    serializer_class = CVDocSerializer
