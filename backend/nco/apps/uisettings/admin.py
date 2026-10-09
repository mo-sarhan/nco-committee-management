from django.contrib import admin
from .models import (
    UiSection,
    UiField,
)

# Register your models here.


class UiFieldInline(admin.TabularInline):
    model = UiField
    extra = 0
    fields = [
        'field_key', 'default_label', 'label', 'display_order', 'visible_flag',
        'label_background', 'label_color',
        'value_background', 'value_color',
        'border_color', 'border_width', 'border_radius',
        'active_flag',
    ]


@admin.register(UiSection)
class UiSectionAdmin(admin.ModelAdmin):
    list_display = ['page_key', 'section_key', 'title', 'display_order', 'visible_flag', 'active_flag']
    list_filter = ['page_key', 'visible_flag', 'active_flag']
    search_fields = ['page_key', 'section_key', 'title']
    ordering = ['page_key', 'display_order']
    inlines = [UiFieldInline]

    def get_queryset(self, request):
        return UiSection.all_objects.all()


@admin.register(UiField)
class UiFieldAdmin(admin.ModelAdmin):
    list_display = ['section', 'field_key', 'label', 'display_order', 'visible_flag', 'active_flag']
    list_filter = ['section__page_key', 'visible_flag', 'active_flag']
    search_fields = ['field_key', 'label']
    ordering = ['section', 'display_order']

    def get_queryset(self, request):
        return UiField.all_objects.select_related('section')
