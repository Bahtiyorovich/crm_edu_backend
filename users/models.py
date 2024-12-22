from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from attendance.models import Attendance
from grades.models import Grade


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_admin(self):
        return self.is_authenticated and self.role == 'admin'

    def is_teacher(self):
        return self.is_authenticated and self.role == 'teacher'

    def is_student(self):
        return self.is_authenticated and self.role == 'student'


class Group(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True, blank=True,
            related_name='teaching_groups',
            limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return f"{self.name} - {self.teacher.username if self.teacher else 'No Teacher'}"

class ClassSchedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='schedules')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True, limit_choices_to={'role': 'teacher'})
    day_of_week = models.CharField(max_length=9, choices=[('odd', 'Odd'), ('even', 'Even')])  # Juft yoki toq kunlar
    time_start = models.TimeField()  # Dars boshlanish vaqti
    time_end = models.TimeField()    # Dars tugash vaqti


class AdminProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='admin_profile'
    )

    def __str__(self):
        return f"Admin profile: {self.user.username}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='teacher_profile'
    )
    admin = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teachers',
        limit_choices_to={'role': 'admin'}  # Only allow linking to admin users
    )
    groups = models.ManyToManyField(Group, related_name='teachers', blank=True)

    def get_students(self):
        # O'qituvchi bilan bog'langan barcha o'quvchilarni olish
        return User.objects.filter(student_profile__group__teachers=self.user)

    def get_student_grades(self, student):
        # O'qituvchining talabasining baholarini olish
        return Grade.objects.filter(student=student, teacher=self.user)

    def get_student_attendance(self, student):
        # O'qituvchining talabasining davomatini olish
        return Attendance.objects.filter(student=student, teacher=self.user)

    def __str__(self):
        return f"Teacher profile: {self.user.username}"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student_profile'
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        limit_choices_to={'role': 'teacher'}  # Only allow linking to teacher users
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
    )

    def __str__(self):
        return f"Student profile: {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'admin':
            AdminProfile.objects.get_or_create(user=instance)
        elif instance.role == 'teacher':
            TeacherProfile.objects.get_or_create(user=instance)
        elif instance.role == 'student':
            StudentProfile.objects.get_or_create(user=instance)
