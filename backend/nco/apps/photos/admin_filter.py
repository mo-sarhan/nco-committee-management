from django.contrib import admin
from datetime import date


class AgeRangeFilter(admin.SimpleListFilter):
    title = 'age range'
    parameter_name = 'age_range'

    def lookups(self, request, model_admin):
        return [
            ('17-','17-'),
            ('18-20','18-20'),
            ('21-25','21-25'),
            ('26-30','26-30'),
            ('31-35','31-35'),
            ('36-40','36-40'),
            ('40+','40+')
        ]

    def queryset(self, request, queryset):
        today = date.today()
        self.lookup_choices
        choices = [ lookup[1] for lookup in  self.lookup_choices ]
        value = self.value()
        # print(choices)
        # print(value)
        if value in choices:
            split_value = value.split('-')
            if len(split_value) > 1:
                min_dob = split_value[0]
                max_dob = split_value[1]
                if max_dob.isdigit():
                    return queryset.filter(mil_ser__birth_date__date__lte = today.replace(year=today.year - int(min_dob)),mil_ser__birth_date__date__gte = today.replace(year=today.year - int(max_dob)))
                else:
                    return queryset.filter(mil_ser__birth_date__date__gte = today.replace(year=today.year - int(min_dob)))
            else:
                max_dob = value.split('+')[0]
                if max_dob.isdigit():
                    return queryset.filter(mil_ser__birth_date__date__lte = today.replace(year=today.year - int(max_dob)))



