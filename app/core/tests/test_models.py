from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@londonappdev.com'
        password = 'Testpass123'

        """ Calling the following get_user_model method actually references the settings file to see what 
            has been set as the user model class (specified by the AUTH_USER_MODEL class). In our case, 
            the user model class is set to the User class (core.User). In the User model, we set the "objects"
            field/attribute to be the UserManager class. We then call the create_user method of that 
            UserManager class to create new users.
        """

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    # the first argument of every class method, including init is always a reference to the current instance of the class
    def test_new_user_email_normalized(self):
        """Test that the email for a new user is normalized"""
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)