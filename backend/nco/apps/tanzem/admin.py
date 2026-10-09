from django.contrib import admin
from .models import ArmyCode,Rank,Jobs

# Register your models here.

class JobsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Jobs._meta.fields]
    search_fields = ['job_name']

class ArmyCodeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ArmyCode._meta.fields]
    search_fields = ['army_code','army_name']

class ArmyCodeInline(admin.TabularInline):
    model = ArmyCode
    list_display = [field.name for field in ArmyCode._meta.fields]
    extra = 0

class RankAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Rank._meta.fields]
    search_fields = ['rank_name']

admin.site.register(ArmyCode,ArmyCodeAdmin)
admin.site.register(Rank,RankAdmin)
admin.site.register(Jobs,JobsAdmin)