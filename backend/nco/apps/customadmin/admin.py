from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.


class PermissionAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in Permission._meta.fields]

admin.site.register(Permission,PermissionAdmin)