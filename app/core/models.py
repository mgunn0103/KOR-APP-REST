from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


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

