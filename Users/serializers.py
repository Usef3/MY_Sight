from rest_framework import serializers
from .models import User, Companion, Patient, Reminder, Location, Task, Notification
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    patient_username = serializers.CharField(write_only=True, required=False)
    relationship = serializers.ChoiceField(
        choices=Companion.RELATIONSHIP_CHOICES,
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'account_type',
            'phone_number', 'name', 'location', 'profile_photo',
            'patient_username', 'relationship'
        )

    def create(self, validated_data): 
        patient_username = validated_data.pop('patient_username', None)
        relationship = validated_data.pop('relationship', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            account_type=validated_data['account_type'],
            phone_number=validated_data.get('phone_number', ''),
            name=validated_data.get('name', ''),
            location=validated_data.get('location', ''),
        )

        # إذا كان من نوع "Companion"، نقوم بتحديث العلاقة وربطه بمريض
        if user.account_type == 'companions':
            companion = user.companions  # تم إنشاؤه تلقائيًا عبر signal
            if patient_username:
                try:
                    patient = Patient.objects.select_related('user').get(user__username=patient_username)
                    companion.patient = patient
                except Patient.DoesNotExist:
                    raise serializers.ValidationError({"patient_username": "Patient not found."})
            if relationship:
                companion.relationship = relationship
            companion.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    patient_username = serializers.CharField(write_only=True, required=False)
    companion_username = serializers.CharField(write_only=True, required=False)
    relationship = serializers.ChoiceField(
        choices=Companion.RELATIONSHIP_CHOICES,
        write_only=True,
        required=False
    )
    related_companion = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'phone_number', 'name', 
            'profile_photo', 'patient_username', 
            'companion_username', 'relationship', 'related_companion'
        )
        read_only_fields = ('username',)

    def get_related_companion(self, obj):
        if hasattr(obj, 'patients'):
            companion = obj.patients.companions.first()
            if companion:
                return {
                    'username': companion.user.username,
                    
                    'relationship': companion.relationship
                }
        return None

class CompanionProfileSerializer(serializers.ModelSerializer):
    
    patient_username = serializers.SlugRelatedField(
        slug_field='user__username',  # نربط بالمريض عن طريق الـ username الخاص بـ user
        queryset=Patient.objects.select_related('user').all(),
        source='patient',
        required=False
    )

    class Meta:
        model = Companion
        fields = (
            'id', 'name', 'email', 'phone_number', 'location',
            'relationship', 'patient_username', 'alert_settings', 'profile_photo'
        )
        read_only_fields = ('email',)


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'email', 'phone_number', 'location', 'medical_condition', 'account_photo', 'current_gps_location', 'additional_notes','companions_username')
        read_only_fields = ('email',)

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'medical_condition', 'account_photo', 'current_gps_location', 'additional_notes']

class CompanionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # تم تغيير حقل patient ليكون اختياريًا ويرتبط عبر SerializerMethodField
    patient_info = serializers.SerializerMethodField()

    class Meta:
        model = Companion
        fields = ['id', 'user', 'patient_info', 'relationship', 'alert_settings']
    
    def get_patient_info(self, obj):
        # إذا كان هناك علاقة مباشرة مع Patient
        if hasattr(obj, 'patient'):
            return obj.patient.id
        # إذا كانت العلاقة تتم عبر User
        elif hasattr(obj.user, 'patient'):
            return obj.user.patient.id
        return None

class ReminderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Reminder
        fields = ['id', 'user', 'transmission_time', 'reminder_message']

class LocationSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

    class Meta:
        model = Location
        fields = ['id', 'gps_coordinates', 'time_coordinates', 'patient']

class TaskSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'task_name', 'task_description', 'reminder_time', 'patient']

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Notification
        fields = ['id', 'user', 'transmission_time', 'notification_type', 'message']



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    def validate(self, attrs):
        data = super().validate(attrs)

        # data.pop("access", None)
        # data.pop("refresh", None)

        user = self.user

        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "account_type": user.account_type,
            "phone_number": user.phone_number,
            "location": user.location,
            "username": user.username,
            "profile_photo": user.profile_photo.url if user.profile_photo else None,
        }

        # لو المستخدم مرافق (Companion)
        if hasattr(user, 'companions'):
            companion = user.companions
            user_data["relationship"] = companion.relationship
           
            user_data["patient_username"] = companion.patient.user.username if companion.patient else None

            # إضافة اسم وإيميل المريض المرتبط
            if companion.patient:
                user_data["linked_patient_type"] = companion.patient.name
                
            else:
                user_data["linked_patient_type"] = None
               

        # لو المستخدم مريض (Patient)
        elif hasattr(user, 'patients'):
            patient = user.patients
            user_data["medical_condition"] = patient.medical_condition
            user_data["account_photo"] = patient.account_photo.url if patient.account_photo else None
            user_data["current_gps_location"] = patient.current_gps_location
            user_data["additional_notes"] = patient.additional_notes

            # إضافة اسم وإيميل أول مرافق مرتبط
            first_companion = patient.companions.first()
            if first_companion:
                user_data["linked_companion_name"] = first_companion.user.username
            else:
                user_data["linked_companion_name"] = None
                

        data["user"] = user_data
        return data

