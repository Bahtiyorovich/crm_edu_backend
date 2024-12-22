from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, AdminProfile, TeacherProfile, StudentProfile, Group
from .serializers import (
    UserSerializer,
    AdminProfileSerializer,
    TeacherProfileSerializer,
    StudentProfileSerializer,
    CustomTokenObtainPairSerializer, GroupSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AdminProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Foydalanuvchi autentifikatsiya qilinmagan.")
        if user.is_admin():
            return AdminProfile.objects.all()
        return AdminProfile.objects.none()


class GroupViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class TeacherProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    def get_queryset(self):
        """Adminlar va o'qituvchilar o'z profillarini ko'rishlari mumkin."""
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Foydalanuvchi autentifikatsiya qilinmagan.")
        if user.is_admin():
            return TeacherProfile.objects.all()
        elif user.is_teacher():
            return TeacherProfile.objects.filter(user=user)
        return TeacherProfile.objects.none()


class StudentProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['teacher', 'user']

    def get_queryset(self):
        """O'qituvchi faqat o'z o'quvchilarini, o'quvchi esa faqat o'z profilini ko'radi."""
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Foydalanuvchi autentifikatsiya qilinmagan.")
        if user.is_admin():
            return StudentProfile.objects.all()
        elif user.is_teacher():
            return StudentProfile.objects.filter(teacher=user)
        elif user.is_student():
            return StudentProfile.objects.filter(user=user)
        return StudentProfile.objects.none()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def role_based_redirect(request):
    """Foydalanuvchi roliga qarab salomlashuvni ko'rsatadi."""
    role_messages = {
        'admin': 'Welcome Admin!',
        'teacher': 'Welcome Teacher!',
        'student': 'Welcome Student!',
    }
    role = getattr(request.user, 'role', None)
    if role in role_messages:
        return Response({'message': role_messages[role]}, status=status.HTTP_200_OK)
    return Response({'message': 'Role not recognized or authorized!'}, status=status.HTTP_403_FORBIDDEN)
