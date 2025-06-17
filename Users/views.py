from rest_framework import generics
from .models import User, Companion, Patient, Reminder, Location, Task, Notification
from .serializers import (
    UserSerializer, CompanionSerializer, PatientSerializer, 
    ReminderSerializer, LocationSerializer, TaskSerializer, NotificationSerializer,
    ProfileSerializer, CompanionProfileSerializer, PatientProfileSerializer,
    CustomTokenObtainPairSerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone

User = get_user_model()

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip()

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email__iexact=email).first()

        if not user:
            return Response({"error": "This email is not registered in our system"}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"https://your-frontend.com/reset-password?uid={uid}&token={token}"

        send_mail(
            "Reset Your Password",
            f"Click the link below to reset your password:\n{reset_link}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "A password reset link has been sent to your email."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return render(request, 'password_reset_confirm.html', {
                'error': 'Invalid or expired password reset link. Please request a new password reset.'
            })

        if not default_token_generator.check_token(user, token):
            return render(request, 'password_reset_confirm.html', {
                'error': 'Invalid or expired password reset link. Please request a new password reset.'
            })

        return render(request, 'password_reset_confirm.html')

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid or expired password reset link. Please request a new password reset."}, 
                          status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired password reset link. Please request a new password reset."}, 
                          status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response({"error": "Both password fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({"error": "Password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed to reset password. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]  

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]  

class CompanionListCreateView(generics.ListCreateAPIView):
    queryset = Companion.objects.all()
    serializer_class = CompanionSerializer
    permission_classes = [AllowAny] 

class CompanionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Companion.objects.all()
    serializer_class = CompanionSerializer
    permission_classes = [AllowAny] 

class ReminderListCreateView(generics.ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [AllowAny] 

class ReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [AllowAny] 

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny] 

class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny] 

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny] 

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny] 

class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny] 

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny] 

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "success": True,
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Handle file upload
        if 'profile_photo' in request.FILES:
            # Delete old photo if exists
            if instance.profile_photo:
                instance.profile_photo.delete()
            # Save new photo
            instance.profile_photo = request.FILES['profile_photo']
            instance.save()

        # Handle other fields
        data = request.data.copy()
        if 'profile_photo' in data:
            del data['profile_photo']  # Remove from data since we handled it separately

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if instance.account_type == 'companions':
            companion = instance.companions
            if 'relationship' in request.data:
                companion.relationship = request.data['relationship']
            if 'patient_username' in request.data:
                try:
                    patient = Patient.objects.get(user__username=request.data['patient_username'])
                    companion.patient = patient
                except Patient.DoesNotExist:
                    return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
            companion.save()

        elif instance.account_type == 'patients':
            patient = instance.patients
            if 'companion_username' in request.data:
                try:
                    companion = Companion.objects.get(user__username=request.data['companion_username'])
                    old_companion = patient.companions.first()
                    if old_companion and old_companion != companion:
                        old_companion.patient = None
                        old_companion.save()
                    companion.patient = patient
                    companion.save()
                except Companion.DoesNotExist:
                    return Response({"error": "Companion not found"}, status=status.HTTP_404_NOT_FOUND)
            patient.save()

        return Response(self.get_serializer(instance).data)

class CompanionProfileUpdateView(generics.UpdateAPIView):
    serializer_class = CompanionProfileSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.companions

    def update(self, request, *args, **kwargs): 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class PatientProfileUpdateView(generics.UpdateAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.patients

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class SOSView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        is_active = request.data.get('is_active', False)

        if not isinstance(is_active, bool):
            return Response(
                {
                    "success": False,
                    "message": "is_active must be true or false"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if user.account_type == 'companions':
                companion = user.companions
                companion.sos_alert = is_active
                if is_active:
                    companion.last_sos_time = timezone.now()
                    # إرسال إشعار للمريض
                    if companion.patient:
                        Notification.objects.create(
                            user=companion.patient.user,
                            transmission_time=timezone.now(),
                            notification_type='security',
                            message=f"تنبيه SOS من {companion.user.name}"
                        )
                companion.save()

                if is_active and not companion.patient:
                    return Response({
                        "success": False,
                        "message": "لا يوجد مريض مرتبط بك"
                    }, status=status.HTTP_400_BAD_REQUEST)

            elif user.account_type == 'patients':
                patient = user.patients
                patient.sos_alert = is_active
                if is_active:
                    patient.last_sos_time = timezone.now()
                    # إرسال إشعار لجميع المرافقين
                    for companion in patient.companions.all():
                        Notification.objects.create(
                            user=companion.user,
                            transmission_time=timezone.now(),
                            notification_type='security',
                            message=f"تنبيه SOS من {patient.user.name}"
                        )
                patient.save()

                if is_active and not patient.companions.exists():
                    return Response({
                        "success": False,
                        "message": "لا يوجد مرافقون مرتبطون بك"
                    }, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({
                    "success": False,
                    "message": "نوع الحساب غير معروف"
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "success": True,
                "message": "تم تفعيل التنبيه بنجاح" if is_active else "تم إيقاف التنبيه بنجاح"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "حدث خطأ أثناء معالجة الطلب"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
