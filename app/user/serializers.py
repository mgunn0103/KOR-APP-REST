from django.contrib.auth import get_user_model, authenticate

"""Allows you to pass output through a tranlations system in case other languages are added"""
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    # must be defined
    class Meta:
        # specifies the model that you want to base your serializer from
        model = get_user_model()

        # Next specify the fields that you want to include in the serializer. 
        # These are the fields that are going to be converted to and from JSON when we make our posts and gets
        # simply add new fields here when ncecesary
        fields =('email', 'password', 'name')

        # next, we are including extra_keyword_args. This allows us toi configure a few extra setting in our model serializer
        # we are going to user this to ensure that the password is write-only and the minimum required lentgh is 5 characters
        extra_kwargs ={'password':{'write_only': True, 'min_length': 5}}

    # overriding the create function 
    def create(self, validated_data): 
        """Create a new user with encrypted password and return it"""
        """ Okay so what we're going to do here is we're going to call 
            the create_user function in our model because by default it only calls the
            create function and we want to use our create user model manager
            function that we created in our models to create the user so we know that the
            password that it stores will be encrypted. Otherwise the password that it sets 
            will just be the cleartext password that we pass in and then
            the authentication won't work because it's expecting an encrypted salt key.
            So this is returning the User model that we specified in the settings file 
            instead of the typical User model.
        """

        # validated_data will contain all of the data tha was passed to the serializer
        # this validated_data will be the JSON data from the POST
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user



class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        # this avoids django default Serializer from trimming whitespace
        trim_whitespace=False
    )

    """ So the validation is basically checking that the inputs are all correct
        so that this is a chart or a character field. And the password is a also a 
        character field as part of the validation function we are also going to
        validate that the authentication credentials are correct. So this is based off 
        the default token serializer that is built into the Django rest framework which
        is modifying it slightly for to accept our e-mail address is that of username.
    """

    # attrs is basically evey field that makes up the serializer
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg=_('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code="authentication")

        attrs['user'] = user
        return attrs



    



