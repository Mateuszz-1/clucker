"""Tests of the sign up view."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from microblogs.forms import SignUpForm
from microblogs.models import User

class SignUpViewTestCase(TestCase):
    """Tests of the sign up view."""

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'first_name': 'George',
            'last_name': 'Ducks',
            'username': '@george',
            'email': 'georgeducks@lemonade.org',
            'bio': 'I run a lemonade stand',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
        }

    def test_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_sign_up(self):
        self.form_input['username'] = "BAD_USERNAME"
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)

    def test_successful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual((before_count + 1), after_count)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        user = User.objects.get(username='@george')
        self.assertEqual(user.first_name, 'George')
        self.assertEqual(user.last_name, 'Ducks')
        self.assertEqual(user.email, 'georgeducks@lemonade.org')
        self.assertEqual(user.bio, 'I run a lemonade stand')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)