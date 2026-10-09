from django.contrib import admin
from django.utils.html import mark_safe,format_html
from .admin_filter import AgeRangeFilter
from .models import (
    PhotoInfo,
    PhotoType,
    PhotoStatusType,
    RejectPhotoReason,
    RejectPhotoInfo
)

# Register your models here.


# ------------------------   actions --------------------------------------
def mark_as_unactive(modeladmin,request,queryset):
    updated = queryset.update(active_flag=False)
    modeladmin.message_user(request,f'{updated} items as updated')

def mark_as_active(modeladmin,request,queryset):
    updated = queryset.update(active_flag=True)
    modeladmin.message_user(request,f'{updated} items as updated')

def set_family_serial_null(modeladmin,request,queryset):
    updated = queryset.update(photo_family_serial=None)
    modeladmin.message_user(request,f'{updated} items as updated')
# --------------------------------------------------------------


class PhotoTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PhotoType._meta.fields]
    # readonly_fields=list_display

class PhotoTypeInline(admin.TabularInline):
    model=PhotoType
    list_display = [field.name for field in PhotoType._meta.fields]
    extra=0
    
class RejectPhotoReasonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RejectPhotoReason._meta.fields]

    
class RejectPhotoReasonInline(admin.TabularInline):
    model=RejectPhotoReason
    list_display = [field.name for field in RejectPhotoReason._meta.fields]
    extra=0




class RejectPhotoInfoAdmin(admin.ModelAdmin):
    list_display =  [field.name for field in RejectPhotoInfo._meta.fields]+['images_tag'] 

    readonly_fields = ['images_tag']
    def images_tag(self,obj):
        html=''
        for image in [obj.photo_id.photo_path]:
            if image:
                html +=f"<a href='{image.url}' target='_blank'><img src='{image.url}' style='height:150px; wigdth:150px;'/></a>"
        return format_html(html or '-')
    images_tag.short_description = "Images"


class RejectPhotoInfoInline(admin.TabularInline):
    model=RejectPhotoInfo
    list_display = [field.name for field in RejectPhotoInfo._meta.fields]
    extra=0


class PhotoInfoAdmin(admin.ModelAdmin):
    # readonly_fields = ['images_tag']
    list_display =['mil_ser__degree_name','mil_ser__marital_state_code','mil_ser__marital_state_name','mil_ser__tot_years','mil_ser__mil_no']+[field.name for field in PhotoInfo._meta.fields] #+['images_tag']  
    search_fields = ['mil_ser__mil_ser','mil_ser__mil_no','mil_ser__person_name']
    autocomplete_fields = ['mil_ser']
    list_filter = ['mil_ser__prnt_army_name','mil_ser__army_name','mil_ser__degree_name','mil_ser__marital_state_name','mil_ser__person_sex_name',AgeRangeFilter,'photo_type_code','photo_family_serial','active_flag','delete_flag','photo_status','create_date']
    
    inlines = [RejectPhotoInfoInline]
    actions = [mark_as_active,mark_as_unactive,set_family_serial_null]

    class Media:
        css = {
            "all":(r'admin/css/image_modal.css',)
        }
        js = (r'admin/js/image_modal.js',)

    def images_tag(self,obj,*args,**kwargs):
        html=''
        for image in [obj.photo_path]:
            if image:
                html +=f"""<div onclick="imagePopup('{image.url}')" onclick.self="clearImagePopup()"><img src='{image.url}' style='height:150px; wigdth:150px;'/></div>"""
                # html=f"""
                #     <div class="modal-overlay">
                #         <div class="modal-content">
                #             <a href='{image.url}' target='_blank'><img src='{image.url}' style='height:150px; wigdth:150px;'/></a>
                #         </div>
                #     </div>""" 

#                 html +=f"""
#                 <a href="{image.url}" onclick="window.open(this.href,'image_popup',width=800,height=600); return false;">
#                 <img src="{image.url}" width="100" height="100"
#                 style="object-fit:cover;" /></a>
# """
#                 html += f"""
#                 <img src="{image.url}" 
#                         class="admin-image-thumbnail"
#                         data-full-image="{image.url}"
#                         style="max-width:150px; cursor:pointer;"/>
# """

        return format_html(html or '-')
    images_tag.short_description = "Images"


class PhotoInfoInline(admin.TabularInline):
    model=PhotoInfo
    list_display= [field.name for field in PhotoInfo._meta.fields] #+['images_tag']
    # readonly_fields = ['images_tag']
    extra=0
    def images_tag(self,obj):
        html=''
        for image in [obj.photo_path]:
            if image:
                html +=f"<a href='{image.url}' target='_blank'><img src='{image.url}' style='height:150px; wigdth:150px;'/></a>"
        return format_html(html or '-')
    images_tag.short_description = "Images"


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(active_flag=True)



class PhotoStatusTypeAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in PhotoStatusType._meta.fields]
    inlines = [PhotoInfoInline]

    

class PhotoStatuTypeInline(admin.TabularInline):
    model = PhotoStatusType
    list_display = [ field.name for field in PhotoStatusType._meta.fields]
    extra = 0

admin.site.register(PhotoType,PhotoTypeAdmin)
admin.site.register(PhotoInfo,PhotoInfoAdmin)
admin.site.register(RejectPhotoReason,RejectPhotoReasonAdmin)
admin.site.register(RejectPhotoInfo,RejectPhotoInfoAdmin)
admin.site.register(PhotoStatusType,PhotoStatusTypeAdmin)