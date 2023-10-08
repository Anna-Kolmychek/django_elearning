from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user1 = User.objects.create(
            email='user1@email.com'
        )
        user1.set_password('12345')
        user1.save()

        user2 = User.objects.create(
            email='user2@email.com'
        )
        user2.set_password('12345')
        user2.save()
