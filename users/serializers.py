from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from grades.serializers import GradeSerializer
from attendance.serializers import AttendanceSerializer
from .models import User, AdminProfile, TeacherProfile, StudentProfile, Group


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Asl JWT tokenni olish
        token = super().get_token(user)

        # Maxsus ma'lumotlarni qo'shish
        token['role'] = user.role  # Foydalanuvchi roli (admin, teacher, student)
        token['user_id'] = user.id  # Foydalanuvchi ID'si
        token['username'] = user.username  # Foydalanuvchi nomi (ixtiyoriy)
        return token

    def validate(self, attrs):
        # Asl tokenni yaratish
        data = super().validate(attrs)

        # Qo'shimcha ma'lumotlarni javobga qo'shish
        data['role'] = self.user.role
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        return data



class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ['id', 'user']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'teacher']


class TeacherProfileSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    grades = GradeSerializer(many=True)
    attendance = AttendanceSerializer(many=True)

    class Meta:
        model = TeacherProfile
        fields = ['id', 'user', 'admin', 'groups', 'grades', 'attendance']


class StudentProfileSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'teacher', 'group']


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'profile')
        read_only_fields = ('role',)  # Role maydonini faqat o'qish uchun qilib qo'yamiz
        ref_name = 'CustomUser'

    def get_profile(self, obj):
        """Return the related profile based on the user's role."""
        if obj.is_admin():
            return AdminProfileSerializer(obj.admin_profile).data
        elif obj.is_teacher():
            return TeacherProfileSerializer(obj.teacher_profile).data
        elif obj.is_student():
            return StudentProfileSerializer(obj.student_profile).data
        return None
