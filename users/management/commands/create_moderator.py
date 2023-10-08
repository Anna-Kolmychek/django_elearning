from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='moderator@email.com',
            is_staff=True,
        )

        group = Group.objects.get(name='moderator_group')
        user.groups.add(group)

        user.set_password('12345')

        user.save()
