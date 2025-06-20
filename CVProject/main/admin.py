from django.contrib import admin

from .models import CVDoc, Project, Skill, RequestLog


class ProjectInline(admin.StackedInline):
    model = Project


class SkillInline(admin.StackedInline):
    model = Skill


@admin.register(CVDoc)
class ComputerAdmin(admin.ModelAdmin):
    inlines = (ProjectInline, SkillInline, )


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'experience', 'cvDoc')
    list_display_links = ('id', 'title', 'experience')
    search_fields = ('title',)


admin.site.register(Project)
admin.site.register(Skill, SkillAdmin)
admin.site.register(RequestLog)

