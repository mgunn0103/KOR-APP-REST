from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings

# Whenever you create a new model, you need to run migrations


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        
        """Creates and saves a new user"""

        if not email:
            raise ValueError('Users must have an email address')

        #specifying **extra_fields ensures that anything extra is captured here
        # normalize_email is a method that comes with the base UserManager class
        user = self.model(email=self.normalize_email(email), **extra_fields) 

        # password is set like this so that it is not passed around in cleartext
        user.set_password(password)

        # this is required for supporting multiple databases
        user.save(using=self.db) 

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # UserManager is assigned to the objects attribute of the model
    objects = UserManager() 

    # the USERNAME_FIELD must be a string (as described in the docs)
    # We are pointing Django to the name of the field that it should use as an identifier
    # The parent class is expecting a string
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    # When specifying the ForeignKey, the first argument is the model that we want to specify the 
    # foreign key off of. 
    # on_delete = models.CASCADE means if you delete this user, just delete
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # this is how you define a string representation of
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

        # this is how you define a string representation of
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # makes the field optional by setting a blank. You only have to check for the single blank value
    link = models.CharField(max_length=255, blank=True)

    # You could also refer to the Models below using the class names without quotes, but there would have 
    # to be a particular order of the classes
    ingredients = models.ManyToManyField('Ingredient')
    ingredients = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

