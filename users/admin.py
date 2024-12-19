from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from attendance.models import Attendance
from grades.models import Grade
from .models import User, AdminProfile, TeacherProfile, StudentProfile, Group, ClassSchedule


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    admin.site.register(ClassSchedule)
    admin.site.register(Grade)
    admin.site.register(Attendance)
    admin.site.register(Group)
    admin.site.register(AdminProfile)
    admin.site.register(TeacherProfile)
    admin.site.register(StudentProfile)
