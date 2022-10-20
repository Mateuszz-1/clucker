from django.core.validators import RegexValidator, EmailValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(
        max_length = 30,
        unique = True,
        validators = [RegexValidator(
            regex = r'^@\w{3,}$',
            message = 'Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(
        max_length = 50,
        blank = False
    )
    last_name = models.CharField(
        max_length = 50,
        blank = False
    )
    email = models.EmailField(
        blank = False,
        unique = True,
        validators = [EmailValidator]
    )
    bio = models.CharField(
        blank = True,
        max_length = 520
    )
