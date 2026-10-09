from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class StyleMixin(models.Model):
    """look and feel columns shared by sections and fields"""

    text_color = models.CharField(max_length=30, null=True, blank=True, db_column='TEXT_COLOR')
    background_color = models.CharField(max_length=30, null=True, blank=True, db_column='BACKGROUND_COLOR')

    border_color = models.CharField(max_length=30, null=True, blank=True, db_column='BORDER_COLOR')
    border_width = models.IntegerField(null=True, blank=True, db_column='BORDER_WIDTH')
    border_style = models.CharField(max_length=20, null=True, blank=True, db_column='BORDER_STYLE')
    border_radius = models.IntegerField(null=True, blank=True, db_column='BORDER_RADIUS')

    font_size = models.IntegerField(null=True, blank=True, db_column='FONT_SIZE')
    font_weight = models.CharField(max_length=20, null=True, blank=True, db_column='FONT_WEIGHT')

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active_flag=True, delete_flag=False)


class UiSection(StyleMixin):
    """one collapsible block of a page (البيانات الأساسية / العقوبات / ...)"""

    section_id = models.BigAutoField(primary_key=True, db_column='SECTION_ID')

    page_key = models.CharField(max_length=100, null=False, db_column='PAGE_KEY')
    section_key = models.CharField(max_length=100, null=False, db_column='SECTION_KEY')
    title = models.CharField(max_length=255, null=True, blank=True, db_column='TITLE')

    display_order = models.IntegerField(default=0, db_column='DISPLAY_ORDER')
    visible_flag = models.BooleanField(default=True, db_column='VISIBLE_FLAG')
    expanded_flag = models.BooleanField(default=True, db_column='EXPANDED_FLAG')

    # grid of the section
    columns_count = models.IntegerField(null=True, blank=True, db_column='COLUMNS_COUNT')
    min_column_width = models.IntegerField(null=True, blank=True, db_column='MIN_COLUMN_WIDTH')
    gap_size = models.IntegerField(null=True, blank=True, db_column='GAP_SIZE')

    # header of the section
    title_color = models.CharField(max_length=30, null=True, blank=True, db_column='TITLE_COLOR')
    title_background = models.CharField(max_length=30, null=True, blank=True, db_column='TITLE_BACKGROUND')

    active_flag = models.BooleanField(default=True, db_column='ACTIVE_FLAG')
    delete_flag = models.BooleanField(default=False, db_column='DELETE_FLAG')

    update_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='ui_sections', db_column='UPDATE_USER',
    )
    update_date = models.DateTimeField(auto_now=True, db_column='UPDATE_DATE')

    objects = ActiveManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        """soft delete"""
        self.active_flag = False
        self.delete_flag = True
        self.save(update_fields=['active_flag', 'delete_flag'])

    def hard_delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.page_key} - {self.title or self.section_key}'

    class Meta:
        managed = getattr(settings, 'MANAGED_MIGRATIONS', False)
        db_table = 'UI_PAGE_SECTION'
        ordering = ['page_key', 'display_order', 'section_id']
        constraints = [
            models.UniqueConstraint(
                fields=['page_key', 'section_key'],
                name='ui_section_page_key_section_key',
            )
        ]
        permissions = [
            ('can_manage_ui_settings', 'can manage ui settings'),
        ]


class UiField(StyleMixin):
    """one label/value card inside a section"""

    field_id = models.BigAutoField(primary_key=True, db_column='FIELD_ID')

    section = models.ForeignKey(
        UiSection, on_delete=models.CASCADE, null=False,
        related_name='fields', db_column='SECTION_ID',
    )
    field_key = models.CharField(max_length=100, null=False, db_column='FIELD_KEY')

    # the wording the page itself uses; kept so a screen that does not carry a
    # field_key can still be matched, and so the settings screen can show the
    # admin what the default is
    default_label = models.CharField(max_length=255, null=True, blank=True, db_column='DEFAULT_LABEL')
    # filled in only when an admin wants to override the wording
    label = models.CharField(max_length=255, null=True, blank=True, db_column='LABEL')

    display_order = models.IntegerField(default=0, db_column='DISPLAY_ORDER')
    visible_flag = models.BooleanField(default=True, db_column='VISIBLE_FLAG')
    col_span = models.IntegerField(null=True, blank=True, db_column='COL_SPAN')

    # the label half of the card
    label_color = models.CharField(max_length=30, null=True, blank=True, db_column='LABEL_COLOR')
    label_background = models.CharField(max_length=30, null=True, blank=True, db_column='LABEL_BACKGROUND')

    # the value half of the card
    value_color = models.CharField(max_length=30, null=True, blank=True, db_column='VALUE_COLOR')
    value_background = models.CharField(max_length=30, null=True, blank=True, db_column='VALUE_BACKGROUND')

    active_flag = models.BooleanField(default=True, db_column='ACTIVE_FLAG')
    delete_flag = models.BooleanField(default=False, db_column='DELETE_FLAG')

    update_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='ui_fields', db_column='UPDATE_USER',
    )
    update_date = models.DateTimeField(auto_now=True, db_column='UPDATE_DATE')

    objects = ActiveManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        """soft delete"""
        self.active_flag = False
        self.delete_flag = True
        self.save(update_fields=['active_flag', 'delete_flag'])

    def hard_delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.section.section_key} - {self.label or self.default_label or self.field_key}'

    class Meta:
        managed = getattr(settings, 'MANAGED_MIGRATIONS', False)
        db_table = 'UI_SECTION_FIELD'
        ordering = ['section', 'display_order', 'field_id']
        constraints = [
            models.UniqueConstraint(
                fields=['section', 'field_key'],
                name='ui_field_section_field_key',
            )
        ]
