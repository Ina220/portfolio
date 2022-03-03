from django.contrib import admin
from .models import User, Project, Message, Profile, Skill
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','is_active','date_joined','is_superuser')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user','title','description','video','created')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user','recipient','sender','title','content','created')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','userImage','backgroundImage','bio')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('id','user','devSkills')



admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill, SkillAdmin)
