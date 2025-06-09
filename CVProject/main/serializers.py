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
    skills = SkillSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
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

    def update(self, cv_doc, validated_data):
        skills_data, projects_data = None, None
        if 'skills' in validated_data:
            skills_data = validated_data.pop('skills')
        if 'projects' in validated_data:
            projects_data = validated_data.pop('projects')

        cv_doc = super().update(cv_doc, validated_data)

        # Overwrite existing skills and projects if such fields are present in request
        if skills_data is not None:
            cv_doc.skills.all().delete()
            for skill in skills_data:
                models.Skill.objects.create(cvDoc=cv_doc, **skill)

        if projects_data is not None:
            cv_doc.projects.all().delete()
            for project in projects_data:
                models.Project.objects.create(cvDoc=cv_doc, **project)

        return cv_doc

