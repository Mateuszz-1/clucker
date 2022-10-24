from django.core.management.base import BaseCommand, CommandError
from ...models import User

class Command(BaseCommand):
    for i in range(1, 100):
        ("user" + str(i)).delete()