from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from ...models import User
import string
import secrets

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        for i in range(1, 100):
            username = "user" + str(i)
            fullname = self.faker.name()
            fullname = fullname.split()
            passwordContuctor = ""
            passwordCharacters = string.ascii_letters + string.digits
            for i in range(secrets.choice(string.digits)):
                passwordContuctor += ''.join(secrets.choice(passwordCharacters))
            user = User.objects.create_user(
                username,
                first_name = fullname[0],
                last_name = fullname[1],
                email = self.faker.email(),
                password = passwordContuctor,
                bio = self.faker.text()
            )
            user.save()

