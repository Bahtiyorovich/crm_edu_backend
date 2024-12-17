from rest_framework import serializers
from .models import Admin, Teacher, Student

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class TeacherSerializer(serializers.ModelSerializer):
    admin = AdminSerializer()  # Admin ma'lumotlarini qo'shish

    class Meta:
        model = Teacher
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'admin']

class StudentSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()  # Teacher ma'lumotlarini qo'shish

    class Meta:
        model = Student
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'teacher']
