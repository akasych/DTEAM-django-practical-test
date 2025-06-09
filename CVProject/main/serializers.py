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
    total_experience = serializers.SerializerMethodField()

    def get_total_experience(self, obj):
        skills = obj.skills.all()
        if not skills:
            return 0
        max_skill = reduce(lambda a, b: a if a.experience > b.experience else b, skills)
        return max_skill.experience

    class Meta:
        model = models.CVDoc
        fields = '__all__'
