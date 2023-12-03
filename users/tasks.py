from datetime import datetime, timezone

from celery import shared_task

from users.models import User


@shared_task
def check_last_login():
    users = User.objects.filter(is_active=True).exclude(is_staff=True)
    for user in users:
        if not user.last_login or (datetime.now(timezone.utc) - user.last_login).days >= 30:
            user.is_active = False
            user.save()

