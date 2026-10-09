from rest_framework import serializers
from .models import (
    UiSection,
    UiField,
)


STYLE_FIELDS = [
    'text_color', 'background_color',
    'border_color', 'border_width', 'border_style', 'border_radius',
    'font_size', 'font_weight',
]


class UiFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = UiField
        fields = [
            'field_id', 'section', 'field_key', 'default_label', 'label',
            'display_order', 'visible_flag', 'col_span',
            'label_color', 'label_background',
            'value_color', 'value_background',
            'active_flag', 'delete_flag',
        ] + STYLE_FIELDS
        read_only_fields = ['field_id']


class UiSectionSerializer(serializers.ModelSerializer):
    fields = UiFieldSerializer(many=True, read_only=True)

    class Meta:
        model = UiSection
        fields = [
            'section_id', 'page_key', 'section_key', 'title',
            'display_order', 'visible_flag', 'expanded_flag',
            'columns_count', 'min_column_width', 'gap_size',
            'title_color', 'title_background',
            'active_flag', 'delete_flag', 'fields',
        ] + STYLE_FIELDS
        read_only_fields = ['section_id']


class ReorderSerializer(serializers.Serializer):
    """[{"id": 3, "display_order": 0}, ...]"""

    id = serializers.IntegerField()
    display_order = serializers.IntegerField()
