from rest_framework import serializers
from .models import User, Companion, Patient, Reminder, Location, Task, Notification
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

        if user.account_type == 'companions':
            companion = user.companions
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
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'profile_photo')

    def validate_phone_number(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already used.")
        return value

    def validate_username(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("This username is already used.")
        return value


class CompanionProfileSerializer(serializers.ModelSerializer):
    patient_username = serializers.SlugRelatedField(
        slug_field='user__username',
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
        fields = (
            'id', 'name', 'email', 'phone_number', 'location',
            'medical_condition', 'account_photo', 'current_gps_location',
            'additional_notes', 'companions_username'
        )
        read_only_fields = ('email',)


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'medical_condition',
            'account_photo', 'current_gps_location', 'additional_notes'
        ]


class CompanionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    patient_info = serializers.SerializerMethodField()

    class Meta:
        model = Companion
        fields = ['id', 'user', 'patient_info', 'relationship', 'alert_settings']

    def get_patient_info(self, obj):
        if hasattr(obj, 'patient'):
            return obj.patient.id
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

        if hasattr(user, 'companions'):
            companion = user.companions
            user_data["relationship"] = companion.relationship
            user_data["patient_username"] = companion.patient.user.username if companion.patient else None

            if companion.patient:
                user_data["linked_patient_type"] = companion.patient.name
            else:
                user_data["linked_patient_type"] = None

        elif hasattr(user, 'patients'):
            patient = user.patients
            user_data["medical_condition"] = patient.medical_condition
            user_data["account_photo"] = patient.account_photo.url if patient.account_photo else None
            user_data["current_gps_location"] = patient.current_gps_location
            user_data["additional_notes"] = patient.additional_notes

            first_companion = patient.companions.first()
            if first_companion:
                user_data["linked_companion_name"] = first_companion.user.username
                user_data["relationship"] = first_companion.relationship
            else:
                user_data["linked_companion_name"] = None
                user_data["relationship"] = None

        data["user"] = user_data
        return data


class SOSSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
    target_id = serializers.IntegerField(read_only=True)  # سيتم تعبئته تلقائياً

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['sender_type'] = user.account_type  # 'patients' أو 'companions'
        return attrs
