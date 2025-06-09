from functools import reduce
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
    total_experience = serializers.SerializerMethodField(method_name='get_total_experience')

    class Meta:
        model = models.CVDoc
        fields = '__all__'

    def get_total_experience(self, obj):
        skills = obj.skills.all()
        if not skills:
            return 0
        max_skill = reduce(lambda a, b: a if a.experience > b.experience else b, skills)
        return max_skill.experience

    def create(self, validated_data):
        skills_data = validated_data.pop('skills')
        projects_data = validated_data.pop('projects')
        cv_doc = models.CVDoc.objects.create(**validated_data)
        for skill in skills_data:
            models.Skill.objects.create(cvDoc=cv_doc, **skill)
        for project in projects_data:
            models.Project.objects.create(cvDoc=cv_doc, **project)
        return cv_doc

    def update(self, instance, validated_data):
        # TODO: implement nested objects update. Ignoring them for now
        validated_data.pop("skills")
        validated_data.pop("projects")

        instance = super().update(instance, validated_data)
        return instance

