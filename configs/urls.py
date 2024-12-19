from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from attendance.views import AttendanceViewSet
from grades.views import GradeViewSet
from users.views import UserViewSet, AdminProfileViewSet, TeacherProfileViewSet, StudentProfileViewSet, \
    role_based_redirect, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

class JWTSchemaGenerator(OpenAPISchemaGenerator):
    def get_security_definitions(self):
        security_definitions = super().get_security_definitions()
        security_definitions['type'] = {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
        return security_definitions


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="CRM_EDU API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="yoqubovsherzod1997@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=JWTSchemaGenerator,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'admins', AdminProfileViewSet)
router.register(r'teachers', TeacherProfileViewSet)
router.register(r'students', StudentProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    path('role-redirect/', role_based_redirect),
]