from django.contrib import admin

from .models import CVDoc, Project, Skill


class ProjectInline(admin.StackedInline):
    model = Project


class SkillInline(admin.StackedInline):
    model = Skill


admin.site.register(Project)
admin.site.register(Skill)


@admin.register(CVDoc)
class ComputerAdmin(admin.ModelAdmin):
    inlines = (ProjectInline, SkillInline, )

