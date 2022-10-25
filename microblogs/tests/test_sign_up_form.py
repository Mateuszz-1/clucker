"""Unit tests of the sign up form."""
from django import forms
from django.test import TestCase
from microblogs.forms import SignUpForm
from microblogs.models import User


class SignUpFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    def setUp(self):
        self.form_input = {
            'first_name': 'George',
            'last_name': 'Ducks',
            'username': '@george',
            'email': 'georgeducks@lemonade.org',
            'bio': 'I run a lemonade stand',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    # Form accepts valid input data
    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Form has the necessary fields
    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    # Form users model Validation
    def test_form_uses_model_validation(self):
        self.form_input['username'] = "badusername"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # New password has correct format
    def test_password_must_contain_uppercase_letter(self):
        self.form_input['new_password'] = "password123"
        self.form_input['password_confirmation'] = "password123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_letter(self):
        self.form_input['new_password'] = "PASSWORD123"
        self.form_input['new_password'] = "PASSWORD123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = "Password"
        self.form_input['new_password'] = "Password"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # New password and password confirmation must be identical
    def test_new_password_and_password_confirmation_are_identical(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['new_password'] = "WrongPassword123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())