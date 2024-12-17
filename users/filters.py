from django_filters import rest_framework as django_filters
from .models import Admin, Teacher, Student

# Umumiy filter class
class CommonUserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        fields = ['username', 'first_name', 'last_name']

# Admin uchun filter
class AdminFilter(CommonUserFilter):
    class Meta(CommonUserFilter.Meta):
        model = Admin

# Teacher uchun filter
class TeacherFilter(CommonUserFilter):
    admin = django_filters.CharFilter(field_name='admin__username', lookup_expr='icontains')  # Admin username filtri

    class Meta(CommonUserFilter.Meta):
        model = Teacher

# Student uchun filter
class StudentFilter(CommonUserFilter):
    teacher = django_filters.CharFilter(field_name='teacher__username', lookup_expr='icontains')  # Teacher username filtri

    class Meta(CommonUserFilter.Meta):
        model = Student
