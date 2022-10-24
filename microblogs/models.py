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

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "blog_posts",
        null = True
    )
    text = models.CharField(
        max_length = 280,
        blank = False,
        null = True
    )
    created_at = models.DateTimeField(
        auto_now = False,
        auto_now_add = True,
        null = True
    )

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.text
