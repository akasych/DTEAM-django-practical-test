from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CVDocSerializer
from .models import CVDoc


class CVDocGetUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CVDoc.objects.all()
    serializer_class = CVDocSerializer
    lookup_url_kwarg = "cv_id"


@api_view(['GET'])
def get_cv_list(request):
    cvs = CVDoc.objects.all().order_by("lastname")
    ser_data = CVDocSerializer(cvs, many=True).data
    return Response(ser_data)

#
# @api_view(['GET'])
# def get_cv_doc(request, cv_id):
#     cv = CVDoc.objects.get(id=cv_id)
#     ser_data = CVDocSerializer(cv, many=False).data
#     return Response(ser_data)


@api_view(['POST'])
def create_cv_doc(request):
    data = request.data
    serializer = CVDocSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
