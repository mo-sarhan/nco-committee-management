from django.contrib import admin
from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
    GroupAdmin as BaseGroupAdmin
    )
from .models import Profile




class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]
    search_fields = ['user__username','user__first_name','prnt_army_code__army_code','prnt_army_code__army_name','army_code__army_name','job__job_name']
    list_filter = ['army_code','prnt_army_code','job']
class ProfileInline(admin.TabularInline):
    model=Profile
    list_display = [field.name for field in Profile._meta.fields]
    extra=0
    can_delete=False


# class UserInline(admin.TabularInline):
#     model = User
#     extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline,]

# # # class GroupAdmin(BaseGroupAdmin):
# # #     inlines =[UserInline]

admin.site.unregister(User)
# admin.site.unregister(Group)
admin.site.register(User,UserAdmin)
# admin.site.register(Group,GroupAdmin)
admin.site.register(Profile,ProfileAdmin)




# Register your models here.


# @admin.register(User)
# class UserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         ('Additional Infromation',{
#             'fields': ( 'mil_no','degree_code','prnt_army_code','prnt_army_name'),
#         }),
#     )

#     add_fieldsets = UserAdmin.add_fieldsets + (
#         ('Additiona Information',{
#             'fields': ('mil_no','degree_code','prnt_army_code'),
#             }),
#     )

#     list_display = ('username','email','mil_no','degree_code','prnt_army_name','prnt_army_code','is_staff','is_superuser')

# # 