from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer

""" Creating a new view. We are going to use the "create API" view that comes with
    the Django rest framework. This is a view that is pre-made for us that allows
    us to easily make an API that creates an object in a database using the serializer
    that we are going to provide
"""

class CreateUserView(generics.CreateAPIView):
    """Create a new user inthe system"""
    
    """ All we need to specify in this view is a class variable that points to the serializer class
        that we want to use to create the object. That's literally all that we need to do for our view.
        That is the beaty of the Django rest framework. It makes it really easy for us to create 
        APIs that do standard behavior like creating objects in the database
    """
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for a user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


