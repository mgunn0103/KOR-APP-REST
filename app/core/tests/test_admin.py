from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse  # allows to generate urls for the django admin page

""" These tests are to test that we can properly manage out custom user model from 
    Django Admin
"""


class AdminSiteTest(TestCase):

    """ This is a setup function. That means that this gets run before the execution of every test
        1. Creates our test client
        2. Make sure the user is logged in 
        3. Create a regular user that , although not authenticated, can be listed in our admin page
    """

    def setUp(self):
        # This assigns values to the properties of self so that they are accessible in the other test
        # The Client class has a lot of features that it would be helpful to know about

        # Create a client
        self.client = Client()

        # Create a user
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@londonappdev.com", 
            password="password123"
        )

        # The force_login method is a helper method that allows you to log a user in with the Django authentication
        self.client.force_login(self.admin_user)

        # This creates spare user that can be used for testing, listing, etc.
        self.user = get_user_model().objects.create_user(
            email="test@londonappdev.com", 
            password="password123",
            name="Test user full name"
        )
   

    """ This will test that users are being listed in our Django admin. 
        The reason that we need this test is because we need to slightly customize
        The Django admin to work with our custom user model. 
        The default User Model expects a username, meaning that the default Django 
        admin will also expect a username which we don't have since we are using the 
        email address only in this app. We are going to need to make changes to admin.py to 
        make sure that it supports our custome user model.
    """ 
    def test_user_listed(self):
        """This Test that users are listed on user page"""
        """ These urls are actually defined in the Django admin documentation. 
            This will generate the url for our list user page.
            The reason that we use this reverse function instead of typing the url manually
            is because if we ever want to change the URL in the future, it prevents us from 
            having to go through and change it everywhere in our test because it should update 
            automatically because of reverse
        """
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        """ assertContains is a Django custom assertions that will check that our HTTP response
            containse a certain item. It also has some additional checks that are so clear from 
            the line below. It checks that the HTTP response was HTTP 200 and it looks into the 
            actual content of this response object and check for the specified contents
        """
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

