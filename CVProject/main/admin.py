from django.contrib import admin

from .models import CVDoc, Project, Skill, RequestLog


class ProjectInline(admin.StackedInline):
    model = Project


class SkillInline(admin.StackedInline):
    model = Skill


admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(RequestLog)


@admin.register(CVDoc)
class ComputerAdmin(admin.ModelAdmin):
    inlines = (ProjectInline, SkillInline, )

