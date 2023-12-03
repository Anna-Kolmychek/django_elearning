from smtplib import SMTPException

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from education.models import Course, Lesson
from subscriptions.models import Subscription
from users.models import User

@shared_task
def send_mails_about_update(pk, model):
    if model == 'Course':
        course = Course.objects.get(pk=pk)
    else:
        print('ищем курс к уроку')
        course = Lesson.objects.get(pk=pk).course

    if course:
        print('начинаем отправку писем')
        subscriptions = Subscription.objects.filter(course=course)
        for subscription in subscriptions:
            try:
                print(f'Начали отправление письма для {subscription.user.email}')
                send_mail(
                    subject='Обновление курса',
                    message=f'Курс {subscription.course.title} был обновлен!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[subscription.user.email],
                )
                print(f'Закончили отправлять письмо для {subscription.user.email}')
            except SMTPException as e:
                print(f'Ошибка отправки письма для {subscription.user.email}')

