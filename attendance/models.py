from django.db import models
from django.conf import settings

class Attendance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_attendances', limit_choices_to={'role': 'teacher'})
    date = models.DateField()  # Davomat sana
    status = models.BooleanField()  # True - qatnashdi, False - qatnashmadi

    def __str__(self):
        return f"{self.student.username} - {self.date} - {'Present' if self.status else 'Absent'}"