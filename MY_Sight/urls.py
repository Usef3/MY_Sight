from django.contrib import admin
from django.urls import path, re_path
from Users import views
from Users.views import (
    PasswordResetRequestView,
    PasswordResetConfirmView,
    UserRegistrationView,
    UserLogoutView,
    CustomTokenObtainPairView,
    SOSView 
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI configuration
schema_view = get_schema_view(
    openapi.Info(
        title="MySight API",
        default_version='v1',
        description="API for MySight smart glasses project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    path('sos/', views.SOSView.as_view(), name='sos'),

    # Swagger Docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Authentication
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('auth/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Users
    path('users/', views.UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    # Patients
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),

    # Companions
    path('companions/', views.CompanionListCreateView.as_view(), name='companion-list'),
    path('companions/<int:pk>/', views.CompanionDetailView.as_view(), name='companion-detail'),

    # Reminders
    path('reminders/', views.ReminderListCreateView.as_view(), name='reminder-list'),
    path('reminders/<int:pk>/', views.ReminderDetailView.as_view(), name='reminder-detail'),

    # Locations
    path('locations/', views.LocationListCreateView.as_view(), name='location-list'),
    path('locations/<int:pk>/', views.LocationDetailView.as_view(), name='location-detail'),

    # Tasks
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),

    # Notifications
    path('notifications/', views.NotificationListCreateView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),

    path('profile/', views.ProfileUpdateView.as_view(), name='profile-update'),
]
