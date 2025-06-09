from rest_framework import serializers
from .models import CVDoc


class CVDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVDoc
        fields = '__all__'
