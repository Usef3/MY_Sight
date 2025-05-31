from django.contrib import admin
from .models import User, Companion, Patient, Reminder, Location, Task, Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'account_type', 'location', 'creation_date')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('account_type', 'creation_date')
    ordering = ('-creation_date',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'medical_condition', 'current_gps_location')
    search_fields = ('user__username', 'medical_condition')
    list_filter = ('medical_condition',)

@admin.register(Companion)
class CompanionAdmin(admin.ModelAdmin):
    list_display = ('user', 'relationship', 'patient_display')

    def patient_display(self, obj):
        # نحاول الحصول على المريض المرتبط بالمرافق عبر المستخدم
        return obj.user.patients.name if hasattr(obj.user, 'patients') else "No Patient"

    patient_display.short_description = "Patient"

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transmission_time', 'reminder_message')
    search_fields = ('user__username', 'reminder_message')
    list_filter = ('transmission_time',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'gps_coordinates', 'time_coordinates', 'patient')
    search_fields = ('gps_coordinates', 'patient__user__username')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'task_description', 'reminder_time', 'patient')
    search_fields = ('task_name', 'patient__user__username')
    list_filter = ('reminder_time',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transmission_time', 'notification_type', 'message')
    search_fields = ('user__username', 'message')
    list_filter = ('notification_type', 'transmission_time')
