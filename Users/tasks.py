# tasks.py
from celery import shared_task
from .models import Task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_task_reminder(task_id):
    try:
        task = Task.objects.get(id=task_id)
        if not task.is_sent:
            # Send email notification
            send_mail(
                f'Task Reminder: {task.title}',
                f'This is a reminder for your task: {task.description}',
                settings.EMAIL_HOST_USER,
                [task.companion.user.email],
                fail_silently=False,
            )
            task.is_sent = True
            task.save()
    except Task.DoesNotExist:
        pass
