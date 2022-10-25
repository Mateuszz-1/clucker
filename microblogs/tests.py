from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import User, Post
from .management.commands.seed import Command as seeder

class UserModelTestCase(TestCase):
    def setUp(self):
        #seeder()
        #seeder.handle()
        self.user = User.objects.create_user(
            '@george',
            first_name = 'George',
            last_name = 'Lemons',
            email = 'georgelemons@apples.org',
            password = 'Password123',
            bio = 'Good day mates, my name is George'
        )
        self.user2 = User.objects.create_user(
            '@logan',
            first_name = 'Logan',
            last_name = 'Grapes',
            email = 'logangrapes@lemonade.org',
            password = 'Password123',
            bio = "Logan. I run a lemonade stand, don't ask me for grapes"
        )

    def test_valid_user(self):
        self._assert_user_is_valid()


    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        self.user.username = '@logan'
        self._assert_user_is_invalid()

    def test_username_must_start_with_at_symbol(self):
        self.user.username = 'george'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphanumericals_after_at(self):
        self.user.username = '@george$'
        self._assert_user_is_invalid()
    
    def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
        self.user.username = '@ge'
        self._assert_user_is_invalid()
    
    def test_username_may_contain_numbers(self):
        self.user.username = '@georg3'
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.user.username = '@@george'
        self._assert_user_is_invalid()

    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_can_be_50_characters_long(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_can_be_50_characters_long(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()
    
    def test_first_name_may_already_exist(self):
        self.user.first_name = 'Logan'
        self._assert_user_is_valid()

    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()
    
    def test_last_name_can_be_50_characters_long(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()
    
    def test_last_name_can_be_50_characters_long(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()
    
    def test_last_name_may_already_exist(self):
        self.user.last_name = 'Grapes'
        self._assert_user_is_valid()
    
    def test_email_must_be_unique(self):
        self.user.email = 'logangrapes@lemonade.org'
        self._assert_user_is_invalid()
    
    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()
    
    def test_email_must_be_standardized(self):
        self.user.email = 'myemail'
        self._assert_user_is_invalid()
    
    def test_email_must_be_standardized(self):
        self.user.email = 'example@myemail'
        self._assert_user_is_invalid()

    def test_email_must_be_standardized(self):
        self.user.email = 'example.org'
        self._assert_user_is_invalid()
    
    def test_email_must_be_standardized(self):
        self.user.email = 'example@my.email.is.this'
        self._assert_user_is_invalid()
    
    def test_email_must_be_standardized(self):
        self.user.email = 'george.lemons@apples.org'
        self._assert_user_is_valid()
    
    def test_bio_may_be_blank(self):
        self.user.bio = ''
        self._assert_user_is_valid()
    
    def test_bio_may_be_not_unique(self):
        self.user.bio = "Logan. I run a lemonade stand, don't ask me for grapes"
        self._assert_user_is_valid()
    
    def test_bio_can_be_520_characters_long(self):
        self.user.bio = "x" * 520
        self._assert_user_is_valid()
    
    def test_bio_can_be_520_characters_long(self):
        self.user.bio = "x" * 521
        self._assert_user_is_invalid()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail("Test user should be valid")

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()


class PostModelTestCase(TestCase):
    def setUp(self):
        # Create user for making Posts
        self.user = User.objects.create_user(
            '@george',
            first_name = 'George',
            last_name = 'Lemons',
            email = 'georgelemons@apples.org',
            password = 'Password123',
            bio = 'Waddle Waddle'
        )
        self.post = Post(
            author = self.user,
            text = "the big orange was in my way",
        )
    
    def test_valid_message(self):
        try:
            self.post.full_clean()
        except ValidationError:
            self.fail("Test message should be valid")
    
    def test_author_must_not_be_blank(self):
        self.post.author = None
        with self.assertRaises(ValidationError):
            self.post.full_clean()
    
    def test_text_must_not_be_blank(self):
        self.post.text = ''
        with self.assertRaises(ValidationError):
            self.post.full_clean()
    
    def test_text_must_not_be_overlong(self):
        self.post.text = 'x' * 281
        with self.assertRaises(ValidationError):
            self.post.full_clean()
    










    """#Deleting user does not delete post - fix needed
    def test_deleting_user_deletes_post(self):
        del self.user1
        print(self.post1.author)
        print(self.post1.text)
        print(self.post1.created_at)
    
    def test_user_can_have_multiple_posts(self):
        self.post2 = Post(
            author = self.user1,
            text = "a big cluck"
        )
        print(self.post2.author)
        self.post3 = Post(
            author = self.user1,
            text = "my third cluck! this is GREAT"
        )
    
    def test_post_text_can_be_280_characters(self):
        self.post = Post(
            author = self.user1,
            text = "x" * 280
        )
    
    def test_post_text_can_be_280_characters(self):
        self.post = Post(
            author = self.user1,
            text = "x" * 281
        )"""