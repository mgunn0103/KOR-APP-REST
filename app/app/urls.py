"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""This is like a base urls file"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # We need to tell app.urls to pass any request that is for "user" to our user.urls
    path('api/user/', include('user.urls')),
    path('api/recipe/', include('recipe.urls')),
    # We need to add a url for our media files
    # By default, the Django development server will serve media files for any static files
    # within our project, however, it does not serve media files by default
    # we need to manually add this in the urls
    # This allows the media url to be available in our development server so we can test uploading 
    # images for recipes without having to set up a separate web server for serving these media files
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


