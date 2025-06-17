from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class User(AbstractUser):
    ACCOUNT_TYPES = [
        ('patients', 'Patients'),
        ('companions', 'Companions'),
    ]
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='companions')  
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, max_length=255)
    

    USERNAME_FIELD = 'email'  # 🔥 اجعل تسجيل الدخول بالبريد الإلكتروني
    REQUIRED_FIELDS = ['username']  # 🔑 نحتاج هذا للحفاظ على التوافق

    groups = None
    user_permissions = None

    def __str__(self):
        return f"{self.name} ({self.account_type})"


class Companion(models.Model):
    RELATIONSHIP_CHOICES = [
        ('parent', 'Parent'),        
        ('sibling', 'Sibling'),      
        ('spouse', 'Spouse'),        
        ('child', 'Child'),          
        ('friend', 'Friend'),        
        ('other', 'Other')           
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='companions')  
    name = models.CharField(max_length=100)
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True, blank=True, related_name='companions')

    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    alert_settings = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='companion_photos/', blank=True, null=True)
    sos_alert = models.BooleanField(default=False)
    last_sos_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Companions: {self.name}"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patients')  
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255, blank=True, null=True)
    medical_condition = models.TextField()
    account_photo = models.ImageField(upload_to='patients_photos/', blank=True, null=True)
    current_gps_location = models.CharField(max_length=255, blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    sos_alert = models.BooleanField(default=False)
    last_sos_time = models.DateTimeField(null=True, blank=True)

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return f"Patients: {self.name}"


#  إنشاء حساب مريض أو مرافق تلقائيًا عند إنشاء المستخدم
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.account_type == 'patients':
            Patient.objects.create(
                user=instance,
                name=instance.name,
                email=instance.email,
                phone_number=instance.phone_number,
                location=instance.location
            )
        elif instance.account_type == 'companions':
            Companion.objects.create(
                user=instance,
                name=instance.name,
                email=instance.email,
                phone_number=instance.phone_number,
                location=instance.location
            )


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    patient = getattr(instance, 'patients', None)
    companion = getattr(instance, 'companions', None)

    if patient:
        patient.name = instance.name
        patient.email = instance.email
        patient.phone_number = instance.phone_number
        patient.location = instance.location
        patient.save()

    if companion:
        companion.name = instance.name
        companion.email = instance.email
        companion.phone_number = instance.phone_number
        companion.location = instance.location
        companion.save()


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    transmission_time = models.DateTimeField()
    reminder_message = models.TextField()

    def __str__(self):
        return f"Reminder for {self.user.username} at {self.transmission_time}"


class Location(models.Model):
    gps_coordinates = models.CharField(max_length=255)
    time_coordinates = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"Location for {self.patient.user.username} at {self.time_coordinates}"


class Task(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='tasks')
    companion = models.ForeignKey(Companion, on_delete=models.CASCADE, related_name='tasks')  # المرافق الذي أنشأ المهمة
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()
    reminder_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)  # هل تم إرسال التذكير؟ لتجنب الإرسال المتكرر

    def __str__(self):
        return f"Task: {self.task_name} for {self.patient.user.username} by {self.companion.name}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('security', 'Security Alert'),
        ('update', 'Update'),
        ('reminder', 'Reminder'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    transmission_time = models.DateTimeField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()

    def __str__(self):
        return f"{self.notification_type} for {self.user.username} at {self.transmission_time}"
    
    
   
    
