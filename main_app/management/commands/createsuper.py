from django.core.management import BaseCommand

from user_app.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin',
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=True,
            phone_number=57365
        )
        user.set_password('57365')
        user.save()
