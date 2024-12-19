from rest_framework import serializers
from grades.models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'student', 'teacher', 'score', 'subject', 'date_assigned']
