from django.test import TestCase

from microblogs.models import User
from microblogs.forms import PostForm

class PostFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            '@george',
            first_name = 'George',
            last_name = 'Lemons',
            email = 'georgelemons@apples.org',
            password = 'Password123',
            bio = 'Good day mates, my name is George',
        )

    def test_valid_post_form(self):
        input = { 'text': 'x' * 280 }
        form = PostForm(data=input)
        self.assertTrue(form.is_valid())
    
    def test_invalid_post_form(self):
        input = { 'text': 'x' * 281 }
        form = PostForm(data=input)
        self.assertFalse(form.is_valid())