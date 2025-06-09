from rest_framework import serializers
from . import models


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Skill
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'


class CVDocSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    projects = ProjectSerializer(many=True)

    class Meta:
        model = models.CVDoc
        fields = '__all__'
