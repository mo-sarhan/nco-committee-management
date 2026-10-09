# -*- coding: utf-8 -*-
"""
Registers the sections / fields the front end already renders, so the settings
screen has something to edit from the first run.

    python manage.py seed_ui_settings
    python manage.py seed_ui_settings --reset            # rewrite order/labels of existing rows
    python manage.py seed_ui_settings --page lagna_presenting
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.uisettings.models import UiSection, UiField


PROFILE_PAGE = 'afr_person_profile'
PRESENTING_PAGE = 'lagna_presenting'

# ---------------------------------------------------------------------------
# the profile screens: views/mainAdmin/afrPersons/profile.vue and
# views/mainAdmin/lagna/specificLagnaPersonProfile.vue
# ---------------------------------------------------------------------------
PROFILE_LAYOUT = [
    {
        'section_key': 'basic',
        'title': 'البيانات الأساسية',
        'fields': [
            ('mil_no', 'الرقم العسكري'),
            ('degree_name', 'الدرجة'),
            ('person_name', 'الاسم'),
            ('army_name', 'السلاح'),
            ('fea_name', 'الفئة'),
            ('unit_name', 'الوحدة'),
            ('to_unit_date', 'تاريــخ الضم علي الوحدة'),
            ('unit_period_service', 'مدة الخدمة بالوحدة'),
            ('prnt_army_name', 'التبعية'),
            ('army_job_name', 'الوظيفة'),
            ('come_in_date', 'تاريخ التطوع'),
            ('rateb_date', 'تاريخ صرف الراتب العالي'),
            ('service_years', 'عدد سنوات الخدمة'),
            ('curr_degree_date', 'تاريخ الترقية الحالية'),
            ('upgrade_date', 'تاريخ الترقي المنتــظر'),
            ('address', 'العنوان المدني'),
            ('birth_date', 'تاريــخ الميــلاد'),
            ('age', 'السن'),
            ('length', 'الطول'),
            ('weight', 'الوزن'),
            ('effecincy_avg', 'متوسط تقرير الكفاءة لاخر ثلاث سنوات'),
            ('over_weight', 'فرق الوزن'),
            ('consistency', 'التناسق'),
            ('education', 'التاهيل'),
        ],
    },
    {
        'section_key': 'punishment',
        'title': 'العقوبات',
        'fields': [
            ('punishment_total', 'العقوبات'),
            ('punishment_not_stay', 'الحجز'),
            ('punishment_stay', 'الحبس'),
            ('punishment_military_court', 'محاكم عسكرية'),
            ('punishment_civil_court', 'محاكم مدنية'),
        ],
    },
    {
        'section_key': 'medical',
        'title': 'الموقف الطبي',
        'fields': [
            ('medical_lagna', 'اللجان الطبية'),
        ],
    },
    {
        'section_key': 'custom_vacation',
        'title': 'الاجازات الخاصة',
        'fields': [
            ('vacation_without_salary', 'الاجازات الخاصة بدون مرتب'),
        ],
    },
    {
        'section_key': 'travel',
        'title': 'موقف السفر',
        'fields': [
            ('travel_count', 'عدد السفريات'),
            ('travel_last_country', 'جهة اخر سفرية'),
            ('travel_from', 'من'),
            ('travel_to', 'الي'),
        ],
    },
    {
        'section_key': 'family',
        'title': 'البيانات الإجتماعية',
        'fields': [
            ('marital_state', 'الحالة الاجتماعية'),
            # the page swaps this wording with the person sex, the default below
            # is only the female variant used for matching
            ('spouse_job', 'مؤهل/وظيفة الزوجة'),
            ('children_count', 'عدد الابناء'),
            ('sons', 'الذكور'),
            ('daughters', 'الاناث'),
            ('father_job', 'مؤهل/وظيفة الوالد'),
            ('mother_job', 'مؤهل/وظيفة الوالدة'),
            ('siblings', 'عدد الاشقاء'),
            ('relatives', 'عدد الاقارب'),
            ('prev_marriages', 'الزيجات السابقة'),
        ],
    },
]


# ---------------------------------------------------------------------------
# the projector screen: views/presentation/presenting/presenting.vue
# it shows the same person but in a five column grid, in its own order, and it
# adds two fields the profile does not show, so it gets its own page
# ---------------------------------------------------------------------------
PRESENTING_LAYOUT = [
    {
        'section_key': 'basic',
        'title': 'البيانات الأساسية',
        'fields': [
            ('mil_no', 'الرقم العسكري'),
            ('come_in_date', 'تاريخ التطوع'),
            ('curr_degree_date', 'تاريخ الترقية الحالية'),
            ('birth_date', 'تاريــخ الميــلاد'),
            ('length', 'الطول'),
            ('degree_name', 'الدرجة'),
            ('rateb_date', 'تاريخ صرف الراتب العالي'),
            ('upgrade_date', 'تاريخ الترقي المنتــظر'),
            ('age', 'السن'),
            ('weight', 'الوزن'),
            ('person_name', 'الاسم'),
            ('service_years', 'عدد سنوات الخدمة'),
            ('education', 'التاهيل'),
            ('address', 'العنوان المدني'),
            ('over_weight', 'فرق الوزن'),
            ('unit_name', 'الوحدة'),
            ('unit_prnt_name', 'تبعية الوحدة'),
            ('to_unit_date', 'تاريــخ الضم علي الوحدة'),
            ('army_name', 'السلاح'),
            ('consistency', 'التناسق'),
            ('army_job_name', 'الوظيفة'),
            ('fea_name', 'الفئة'),
            ('unit_period_service', 'مدة الخدمة بالوحدة'),
            ('security_status', 'الموقف الامنــي'),
            ('effecincy_avg', 'متوسط تقرير الكفاءة لاخر ثلاث سنوات'),
        ],
    },
    {
        'section_key': 'punishment',
        'title': 'العقوبات',
        'fields': [
            ('punishment_total', 'العقوبات'),
            ('punishment_not_stay', 'الحجز'),
            ('punishment_stay', 'الحبس'),
            ('punishment_military_court', 'المحكمة'),
            ('punishment_civil_court', 'المحكمة المدنية'),
        ],
    },
    {
        'section_key': 'medical',
        'title': 'الموقف الطبي',
        'fields': [
            ('medical_lagna', 'اللجان الطبية'),
        ],
    },
    {
        'section_key': 'custom_vacation',
        'title': 'الاجازات الخاصة',
        'fields': [
            ('vacation_without_salary', 'الاجازات الخاصة'),
        ],
    },
    {
        'section_key': 'travel',
        'title': 'موقف السفر',
        'fields': [
            ('travel_count', 'عدد السفريات'),
            ('travel_last_country', 'جهة اخر سفرية'),
            ('travel_from', 'من'),
            ('travel_to', 'الي'),
        ],
    },
    {
        # سبب العرض, only rendered for لجان عدم الصلاحية (committee type 1)
        'section_key': 'presenting_reason',
        'title': 'سبب العرض',
        'fields': [
            ('presenting_reason', 'سبب العرض'),
        ],
    },
    {
        # the screen names this block ملخص الاراء for لجان عدم الصلاحية and
        # الاسباب for every other committee, so no title is seeded here; typing
        # one in the settings screen pins it to a fixed name instead
        'section_key': 'reasons',
        'title': None,
        'fields': [
            ('reasons_summary', 'الاسباب / ملخص الاراء'),
        ],
    },
    {
        'section_key': 'family',
        'title': 'البيانات الإجتماعية',
        'fields': [
            ('marital_state', 'الحالة الاجتماعية'),
            # the page swaps this wording with the person sex
            ('spouse_job', 'مؤهل/وظيفة الزوجة'),
            ('children_count', 'عدد الابناء'),
            ('sons', 'الذكور'),
            ('daughters', 'الاناث'),
            ('father_job', 'مؤهل/وظيفة الوالد'),
            ('mother_job', 'مؤهل/وظيفة الوالدة'),
            ('siblings', 'عدد الاشقاء'),
            ('relatives', 'عدد الاقارب'),
            ('prev_marriages', 'الزيجات السابقة'),
        ],
    },
    {
        # one card per committee opinion, built per person
        'section_key': 'lagna_decisions',
        'title': 'الآراء',
        'fields': [],
    },
]


PAGES = [
    (PROFILE_PAGE, PROFILE_LAYOUT),
    (PRESENTING_PAGE, PRESENTING_LAYOUT),
]


class Command(BaseCommand):
    help = 'seed the ui settings tables with the sections/fields the front end renders'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='overwrite title and display_order of rows that already exist',
        )
        parser.add_argument(
            '--page', dest='page',
            help='seed one page only (afr_person_profile / lagna_presenting)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        reset = options['reset']
        only = options.get('page')

        for page_key, layout in PAGES:
            if only and page_key != only:
                continue
            sections, fields = self.seed_page(page_key, layout, reset)
            self.stdout.write(self.style.SUCCESS(
                f'{page_key}: sections created {sections} , fields created {fields}'
            ))

    def seed_page(self, page_key, layout, reset):
        created_sections = created_fields = 0

        for order, block in enumerate(layout):
            section, is_new = UiSection.all_objects.get_or_create(
                page_key=page_key,
                section_key=block['section_key'],
                defaults={'title': block['title'], 'display_order': order},
            )
            created_sections += int(is_new)

            if reset and not is_new:
                section.title = block['title']
                section.display_order = order
                section.active_flag = True
                section.delete_flag = False
                section.save()

            for field_order, (key, label) in enumerate(block['fields']):
                field, is_new = UiField.all_objects.get_or_create(
                    section=section,
                    field_key=key,
                    defaults={'default_label': label, 'display_order': field_order},
                )
                created_fields += int(is_new)

                if reset and not is_new:
                    # default_label follows the code, label belongs to the admin
                    field.default_label = label
                    field.display_order = field_order
                    field.active_flag = True
                    field.delete_flag = False
                    field.save()

        return created_sections, created_fields
