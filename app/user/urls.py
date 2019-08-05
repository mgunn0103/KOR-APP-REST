# this is a helper function that comes from django that allows us to define different paths
from django.urls import path

#importing our own user views
from user import views

# define our app name. 
# This is used to specify what app we are creating the url from when we use user our reverse 
# function

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name="create"),
    path('token/', views.CreateTokenView.as_view(), name="token")
]

