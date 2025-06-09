from rest_framework import serializers
from . import models


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Skill
        fields = ('title', 'experience')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ('title', 'description', 'startDate', 'endDate')


class CVDocSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    projects = ProjectSerializer(many=True)

    class Meta:
        model = models.CVDoc
        fields = '__all__'
