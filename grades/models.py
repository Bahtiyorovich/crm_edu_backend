from django.conf import settings
from django.db import models

class Grade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grades')
    teacher = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
            blank=True, null=True,
            related_name='teacher',
            limit_choices_to={'role': 'teacher'})
    score = models.IntegerField(default=0)
    subject = models.CharField(max_length=100)
    date_assigned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject} - {self.score}"